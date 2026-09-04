"""CPU-only analysis of materialized canonical corpora.

This module deliberately reports availability separately from measurements.  It never
turns an absent reference corpus, tokenizer manifest, or held-out split into zero.
"""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

from opengrad.data.audit import coverage_report
from opengrad.data.normalize import fingerprints


def _restore_row(row: dict[str, Any]) -> dict[str, Any]:
    restored = dict(row)
    for key in ("tools", "messages", "metadata", "context", "chosen", "rejected"):
        value = restored.get(key)
        if isinstance(value, str):
            try:
                restored[key] = json.loads(value)
            except json.JSONDecodeError:
                pass
    return restored


def _rows(value: Iterable[dict[str, Any]] | Path) -> list[dict[str, Any]]:
    if isinstance(value, Path):
        if value.is_dir() and (value / "manifest.json").exists():
            from opengrad.data.materialize import iter_materialized_rows

            return [_restore_row(row) for row in iter_materialized_rows(value)]
        if value.suffix.lower() == ".parquet":
            try:
                import pyarrow.parquet as pq  # type: ignore[import-untyped]
            except ImportError as exc:
                raise RuntimeError(
                    "parquet_reader_unavailable: install the optional data reader"
                ) from exc
            result: list[dict[str, Any]] = []
            for batch in pq.ParquetFile(value).iter_batches(batch_size=128):
                result.extend(_restore_row(row) for row in batch.to_pylist())
            return result
        jsonl_rows: list[dict[str, Any]] = []
        with value.open(encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    item = json.loads(line)
                    if not isinstance(item, dict):
                        raise ValueError("corpus row must be an object")
                    jsonl_rows.append(_restore_row(item))
        return jsonl_rows
    return list(value)


def _overlap_matrix(groups: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    keys = ("raw_hash", "canonical_hash", "conversation", "user_prompt", "tool_catalogue")
    # Empty fingerprints mean "not available", not a shared value.
    indexed = {
        source: {key: {value for row in rows if (value := fingerprints(row)[key])} for key in keys}
        for source, rows in groups.items()
    }
    pairs: dict[str, dict[str, int]] = {}
    sources = list(groups)
    for left_index, left in enumerate(sources):
        for right in sources[left_index + 1 :]:
            pairs[f"{left}__{right}"] = {
                key: len(indexed[left][key] & indexed[right][key]) for key in keys
            }
    matrix = {key: {source: {other: 0 for other in sources} for source in sources} for key in keys}
    for pair, values in pairs.items():
        left, right = pair.split("__", 1)
        for key, count in values.items():
            matrix[key][left][right] = count
            matrix[key][right][left] = count
    return {"status": "MEASURED", "keys": list(keys), "pairs": pairs, "matrix": matrix, **pairs}


def source_quality(rows: list[dict[str, Any]]) -> dict[str, Any]:
    statuses = Counter(str(r.get("metadata", {}).get("parse_status", "VALID")) for r in rows)
    duplicates = sum(
        1 for r in rows if str(r.get("metadata", {}).get("parse_status")) == "DUPLICATE"
    )
    return {
        "status": "MEASURED",
        "records": len(rows),
        "parse_status_counts": dict(statuses),
        "duplicate_records": duplicates,
        "source_fields_observed": sorted(
            {f for r in rows for f in r.get("metadata", {}).get("source_fields", [])}
        ),
    }


def contamination_report(
    rows: list[dict[str, Any]], reference: list[dict[str, Any]] | None = None
) -> dict[str, Any]:
    if reference is None:
        return {
            "status": "BLOCKED",
            "reason": "independent_reference_corpus_missing",
            "matches": None,
        }
    refs = {fingerprints(r)["conversation"] for r in reference}
    matches = [str(r.get("id", "")) for r in rows if fingerprints(r)["conversation"] in refs]
    return {
        "status": "MEASURED",
        "reference_records": len(reference),
        "matches": len(matches),
        "matched_ids": matches,
    }


def build_clean_sft_index(rows: list[dict[str, Any]]) -> dict[str, Any]:
    clean: list[str] = []
    blocked: list[str] = []
    excluded: list[str] = []
    non_sft = {"preference", "mcq", "mcq_test", "llm_judge", "llm_judge_test"}
    for row in rows:
        identifier = str(row.get("id", ""))
        metadata = row.get("metadata", {})
        split = str(metadata.get("split", ""))
        contamination = str(metadata.get("contamination_status", "UNASSESSED"))
        if split in non_sft:
            excluded.append(identifier)
        elif contamination == "CLEAN":
            clean.append(identifier)
        else:
            blocked.append(identifier)
    return {
        "status": "MEASURED" if not blocked else "BLOCKED",
        "clean_candidate_ids": clean,
        "blocked_ids": blocked,
        "excluded_non_sft_ids": excluded,
        "reason": "contamination_unassessed" if blocked else None,
    }


def lineage_status(render_manifest: Path, token_manifest: Path) -> dict[str, Any]:
    reasons: list[str] = []
    for path, reason in (
        (render_manifest, "render_manifest_missing"),
        (token_manifest, "token_manifest_missing"),
    ):
        if not path.exists():
            reasons.append(reason)
    if reasons:
        return {"status": "BLOCKED", "reasons": reasons}
    try:
        render = json.loads(render_manifest.read_text(encoding="utf-8"))
        token = json.loads(token_manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"status": "BLOCKED", "reasons": ["manifest_invalid"]}
    required_render = {"model_id", "model_revision", "renderer", "chat_template_hash"}
    required_token = {"tokenizer_revision", "records"}
    missing = sorted((required_render - render.keys()) | (required_token - token.keys()))
    if missing:
        return {"status": "BLOCKED", "reasons": ["manifest_fields_missing"], "missing": missing}
    return {
        "status": "MEASURED",
        "render_manifest": str(render_manifest),
        "token_manifest": str(token_manifest),
    }


def heldout_readiness(evaluation_rows: list[dict[str, Any]] | None) -> dict[str, Any]:
    if evaluation_rows is None:
        return {"status": "BLOCKED", "reason": "heldout_evaluation_corpus_missing"}
    if not evaluation_rows:
        return {"status": "BLOCKED", "reason": "heldout_evaluation_corpus_empty"}
    return {
        "status": "READY",
        "records": len(evaluation_rows),
        "independent_namespace_required": True,
    }


def analyze_corpus(groups: Mapping[str, Iterable[dict[str, Any]] | Path]) -> dict[str, Any]:
    materialized = {name: _rows(rows) for name, rows in groups.items()}
    all_rows = [row for rows in materialized.values() for row in rows]
    return {
        "status": "MEASURED" if all_rows else "BLOCKED",
        "groups": {
            name: {"records": len(rows), "source_quality": source_quality(rows)}
            for name, rows in materialized.items()
        },
        "overlap": _overlap_matrix(materialized)
        if materialized
        else {"status": "BLOCKED", "reason": "no_corpus"},
        "behavioral_coverage": coverage_report(all_rows)
        if all_rows
        else {"status": "BLOCKED", "reason": "no_corpus"},
        "source_quality": {name: source_quality(rows) for name, rows in materialized.items()},
        "contamination": contamination_report(all_rows),
        "clean_sft": build_clean_sft_index(all_rows),
        "heldout_evaluation": heldout_readiness(None),
    }
