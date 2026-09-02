from collections import Counter
from typing import Any


def stats(records: list[dict[str, Any]]) -> dict[str, Any]:
    turns = [len(r.get("messages", [])) for r in records]
    calls = sum(
        len(m.get("tool_calls", []))
        for r in records
        for m in r.get("messages", [])
        if m.get("role") == "assistant"
    )
    return {
        "samples": len(records),
        "turns": sum(turns),
        "mean_turns": sum(turns) / len(turns) if turns else 0,
        "tool_calls": calls,
        "calls_per_sample": calls / len(records) if records else 0,
        "sources": dict(Counter(r.get("source", "unknown") for r in records)),
    }


def mixture(records: list[dict[str, Any]], by: str = "samples") -> dict[str, float]:
    counts = Counter(r.get("source", "unknown") for r in records)
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()} if total else {}
