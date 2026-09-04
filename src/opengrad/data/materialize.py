from __future__ import annotations

import hashlib
import json
import os
from collections import Counter
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from opengrad.data.adapters import (
    ADAPTERS,
    adapt_when2call_evaluation,
    adapt_when2call_preference,
)
from opengrad.data.canonical import canonical_dict, stable_json

_VALID_MODES = {"sft", "preference", "evaluation"}


def _source_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _jsonable(value: Any) -> dict[str, Any]:
    if hasattr(value, "__dataclass_fields__"):
        return {name: getattr(value, name) for name in value.__dataclass_fields__}
    if isinstance(value, dict):
        return value
    raise TypeError("adapter did not return a serializable canonical record")


def _row_bytes(row: dict[str, Any]) -> bytes:
    return (stable_json(row) + "\n").encode("utf-8")


def _storage_row(row: dict[str, Any]) -> dict[str, Any]:
    """Use JSON columns for nested IR values so heterogeneous source rows fit one schema."""
    return {
        key: stable_json(value) if isinstance(value, (dict, list)) else value
        for key, value in row.items()
    }


def _write_shard(
    rows: list[dict[str, Any]], destination: Path, checksum: str, source_end: int
) -> None:
    import pyarrow as pa  # type: ignore[import-untyped]
    import pyarrow.parquet as pq  # type: ignore[import-untyped]

    table = pa.Table.from_pylist(rows)
    metadata = dict(table.schema.metadata or {})
    metadata[b"opengrad_row_checksum"] = checksum.encode("ascii")
    metadata[b"opengrad_row_count"] = str(len(rows)).encode("ascii")
    metadata[b"opengrad_source_end"] = str(source_end).encode("ascii")
    table = table.replace_schema_metadata(metadata)
    temporary = destination.with_name(destination.name + ".tmp")
    try:
        pq.write_table(
            table,
            temporary,
            compression="zstd",
            use_dictionary=True,
            write_statistics=False,
            version="2.6",
        )
        with temporary.open("rb+") as handle:
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def _read_valid_shard(path: Path) -> tuple[int, int, str] | None:
    import pyarrow.parquet as pq

    try:
        table = pq.read_table(path)
        metadata = table.schema.metadata or {}
        expected = metadata.get(b"opengrad_row_checksum", b"").decode("ascii")
        expected_count = int(metadata.get(b"opengrad_row_count", b"-1"))
        source_end = int(metadata.get(b"opengrad_source_end", b"-1"))
        rows = table.to_pylist()
        digest = hashlib.sha256(b"".join(_row_bytes(row) for row in rows)).hexdigest()
        if expected_count != len(rows) or source_end < 0 or not expected or digest != expected:
            return None
        return len(rows), source_end, digest
    except (OSError, ValueError, TypeError, EOFError):
        return None


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_name(path.name + ".tmp")
    try:
        temporary.write_text(
            json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8"
        )
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _adapter(dataset: str, split: str, mode: str) -> Any:
    if mode == "preference":
        if dataset != "when2call":
            raise ValueError("preference mode is only supported for when2call")
        return adapt_when2call_preference
    if mode == "evaluation":
        if dataset != "when2call":
            raise ValueError("evaluation mode is only supported for when2call")
        return adapt_when2call_evaluation
    if dataset not in ADAPTERS:
        raise ValueError(f"unknown dataset: {dataset}")
    return ADAPTERS[dataset]


def materialize_parquet(
    input_path: Path,
    output_dir: Path,
    *,
    dataset: str,
    split: str,
    mode: str = "sft",
    shard_size: int = 1000,
    batch_size: int = 128,
    max_records: int | None = None,
) -> dict[str, Any]:
    """Stream a Parquet source into resumable, atomic canonical Parquet shards."""
    if mode not in _VALID_MODES:
        raise ValueError(f"mode must be one of {sorted(_VALID_MODES)}")
    if shard_size < 1 or batch_size < 1:
        raise ValueError("shard_size and batch_size must be positive")
    if max_records is not None and max_records < 0:
        raise ValueError("max_records must be non-negative")
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    source_sha = _source_digest(input_path)
    config = {
        "dataset": dataset,
        "split": split,
        "mode": mode,
        "adapter_version": "1.0.2",
        "shard_size": shard_size,
        "batch_size": batch_size,
        "max_records": max_records,
        "source_sha256": source_sha,
    }
    manifest_path = output_dir / "manifest.json"
    old_manifest: dict[str, Any] = {}
    if manifest_path.exists():
        try:
            old_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            old_manifest = {}
    compatible = old_manifest.get("config") == config

    valid_shards: list[str] = []
    offset = 0
    if compatible:
        index = 0
        while True:
            name = f"shard-{index:06d}.parquet"
            path = output_dir / name
            if not path.exists():
                break
            valid = _read_valid_shard(path)
            if valid is None or valid[0] > shard_size:
                break
            valid_shards.append(name)
            offset = valid[1]
            index += 1
    # A missing/corrupt shard invalidates it and every later shard.
    for path in output_dir.glob("shard-*.parquet"):
        if path.name not in valid_shards:
            path.unlink(missing_ok=True)
    for path in output_dir.glob("shard-*.parquet.tmp"):
        path.unlink(missing_ok=True)

    import pyarrow.parquet as pq

    adapter = _adapter(dataset, split, mode)
    seen_hashes: set[str] = set()
    for name in valid_shards:
        for batch in pq.ParquetFile(output_dir / name).iter_batches(batch_size=128):
            for row in batch.to_pylist():
                if isinstance(row.get("canonical_hash"), str):
                    seen_hashes.add(row["canonical_hash"])
    total_rows = pq.ParquetFile(input_path).metadata.num_rows
    if compatible and offset == (max_records if max_records is not None else total_rows):
        return {"manifest": old_manifest, "manifest_path": str(manifest_path)}
    counts: Counter[str] = Counter()
    counts["resumed_rows"] = offset
    counts["source_rows"] = offset
    counts["valid"] = offset
    rows: list[dict[str, Any]] = []
    shard_index = len(valid_shards)
    source_index = 0
    for batch in pq.ParquetFile(input_path).iter_batches(batch_size=batch_size):
        for raw in batch.to_pylist():
            if source_index < offset:
                source_index += 1
                continue
            if max_records is not None and source_index >= max_records:
                break
            source_index += 1
            counts["source_rows"] += 1
            try:
                if mode == "sft":
                    item = canonical_dict(adapter(raw, split))
                else:
                    item = _jsonable(adapter(raw, split))
                stored = _storage_row(item)
                canonical_hash = stored.get("canonical_hash")
                if isinstance(canonical_hash, str) and canonical_hash in seen_hashes:
                    counts["canonical_duplicates"] += 1
                    continue
                if isinstance(canonical_hash, str):
                    seen_hashes.add(canonical_hash)
                rows.append(stored)
                counts["valid"] += 1
            except (TypeError, ValueError, json.JSONDecodeError):
                counts["parse_failed"] += 1
            if len(rows) >= shard_size:
                digest = hashlib.sha256(b"".join(_row_bytes(row) for row in rows)).hexdigest()
                name = f"shard-{shard_index:06d}.parquet"
                _write_shard(rows, output_dir / name, digest, source_index)
                valid_shards.append(name)
                shard_index += 1
                checkpoint = {
                    "manifest_version": 2,
                    "materializer": "opengrad.data.materialize.materialize_parquet",
                    "config": config,
                    "mode": mode,
                    "shards": valid_shards,
                    "counts": dict(counts),
                }
                _atomic_json(manifest_path, checkpoint)
                rows = []
        if max_records is not None and source_index >= max_records:
            break
    if rows:
        digest = hashlib.sha256(b"".join(_row_bytes(row) for row in rows)).hexdigest()
        name = f"shard-{shard_index:06d}.parquet"
        _write_shard(rows, output_dir / name, digest, source_index)
        valid_shards.append(name)

    counts["shards"] = len(valid_shards)
    counts["training_eligible"] = counts["valid"] if mode == "sft" else 0
    counts["preference_only"] = counts["valid"] if mode == "preference" else 0
    counts["evaluation_only"] = counts["valid"] if mode == "evaluation" else 0
    manifest = {
        "manifest_version": 2,
        "materializer": "opengrad.data.materialize.materialize_parquet",
        "config": config,
        "mode": mode,
        "shards": valid_shards,
        "counts": dict(counts),
    }
    _atomic_json(manifest_path, manifest)
    return {"manifest": manifest, "manifest_path": str(manifest_path)}


def iter_materialized_rows(output_dir: Path) -> Iterator[dict[str, Any]]:
    import pyarrow.parquet as pq

    manifest = json.loads((Path(output_dir) / "manifest.json").read_text(encoding="utf-8"))
    for name in manifest["shards"]:
        parquet = pq.ParquetFile(Path(output_dir) / name)
        for batch in parquet.iter_batches(batch_size=128):
            yield from batch.to_pylist()
