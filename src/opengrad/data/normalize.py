from __future__ import annotations

import hashlib
import json
from collections import Counter
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from opengrad.data.adapters import ADAPTERS
from opengrad.data.canonical import canonical_dict


def iter_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            if line.strip():
                value = json.loads(line)
                if not isinstance(value, dict):
                    raise ValueError(f"line {number} is not an object")
                yield value


def normalize_records(
    records: Iterable[dict[str, Any]],
    dataset: str,
    split: str = "train",
    max_records: int | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    adapter = ADAPTERS[dataset]
    output: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    hashes: set[str] = set()
    for number, record in enumerate(records):
        if max_records is not None and number >= max_records:
            break
        counts["source_rows"] += 1
        try:
            item = canonical_dict(adapter(record, split))
            item_hash = item["canonical_hash"]
            if item_hash in hashes:
                counts["duplicates"] += 1
                counts["status_DUPLICATE"] += 1
                continue
            hashes.add(item_hash)
            output.append(item)
            counts["parsed_rows"] += 1
            counts["valid"] += 1
        except (TypeError, ValueError, json.JSONDecodeError) as exc:
            counts["parse_failed"] += 1
            counts[f"failure_{str(exc).split(':', 1)[0]}"] += 1
    counts["training_eligible"] = sum(
        1
        for x in output
        if split not in {"preference", "mcq", "mcq_test", "llm_judge", "llm_judge_test"}
    )
    counts["evaluation_only"] = counts["source_rows"] - counts["training_eligible"]
    return output, dict(counts)


def write_jsonl(records: Iterable[dict[str, Any]], output: Path) -> str:
    output.parent.mkdir(parents=True, exist_ok=True)
    tmp = output.with_suffix(output.suffix + ".tmp")
    digest = hashlib.sha256()
    with tmp.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            line = (
                json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
            )
            handle.write(line)
            digest.update(line.encode("utf-8"))
    tmp.replace(output)
    return digest.hexdigest()


def report(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = list(records)
    decisions: Counter[str] = Counter()
    sources: Counter[str] = Counter()
    shapes: Counter[str] = Counter()
    capabilities: Counter[str] = Counter()
    observations = 0
    calls = 0
    for row in rows:
        sources[str(row.get("source", "UNKNOWN"))] += 1
        behavior = row.get("metadata", {}).get("behavior", {})
        decisions[str(behavior.get("decision", "UNKNOWN"))] += 1
        messages = row.get("messages", [])
        shapes["multi_turn" if len(messages) > 3 else "single_turn"] += 1
        for message in messages:
            if message.get("role") == "tool":
                observations += 1
            if message.get("role") == "assistant":
                calls += len(message.get("tool_calls", []))
        values = row.get("metadata", {}).get("behavior", {}).get("capabilities", [])
        if isinstance(values, list):
            capabilities.update(str(value) for value in values)
    return {
        "records": len(rows),
        "sources": dict(sources),
        "behavior": dict(decisions),
        "turn_shape": dict(shapes),
        "tool_calls": calls,
        "observations": observations,
        "capabilities": dict(capabilities),
    }


def fingerprints(record: dict[str, Any]) -> dict[str, str]:
    messages = record.get("messages", [])
    user = "\n".join(str(m.get("content", "")) for m in messages if m.get("role") == "user")
    conversation = {"tools": record.get("tools", []), "messages": messages}
    return {
        "raw_hash": str(record.get("metadata", {}).get("raw_record_hash", "")),
        "canonical_hash": str(record.get("canonical_hash", "")),
        "conversation": hashlib.sha256(
            json.dumps(conversation, ensure_ascii=False, sort_keys=True).encode()
        ).hexdigest(),
        "user_prompt": hashlib.sha256(" ".join(user.split()).casefold().encode()).hexdigest(),
        "tool_catalogue": hashlib.sha256(
            json.dumps(record.get("tools", []), ensure_ascii=False, sort_keys=True).encode()
        ).hexdigest(),
    }


def overlap_report(groups: dict[str, Iterable[dict[str, Any]]]) -> dict[str, Any]:
    indexed: dict[str, dict[str, set[str]]] = {}
    for source, rows in groups.items():
        indexed[source] = {
            key: {fingerprints(row)[key] for row in rows}
            for key in (
                "raw_hash",
                "canonical_hash",
                "conversation",
                "user_prompt",
                "tool_catalogue",
            )
        }
    result: dict[str, Any] = {}
    sources = list(indexed)
    for left_index, left in enumerate(sources):
        for right in sources[left_index + 1 :]:
            result[f"{left}__{right}"] = {
                key: len(indexed[left][key] & indexed[right][key]) for key in indexed[left]
            }
    return result


def build_manifest(
    *,
    commit: str,
    dataset: str,
    revision: str,
    adapter: str,
    adapter_version: str,
    config: dict[str, Any],
    counts: dict[str, Any],
    output: str,
    checksum: str,
) -> dict[str, Any]:
    return {
        "manifest_version": 1,
        "opengrad_git_commit": commit,
        "dataset": dataset,
        "dataset_revision": revision,
        "adapter": adapter,
        "adapter_version": adapter_version,
        "canonical_schema_version": "tool_use_ir_v1",
        "behavior_taxonomy_version": "tool-use-behavior-taxonomy-v1",
        "normalization_config": config,
        "counts": counts,
        "output": output,
        "canonical_checksum": checksum,
        "dedup": {"exact": True},
        "contamination": {"status": "UNASSESSED"},
    }
