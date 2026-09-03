from collections import Counter, defaultdict
from typing import Any

DECISIONS = ("CALL", "ANSWER", "CLARIFY", "UNSUPPORTED")


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


def analyze(
    records: list[dict[str, Any]], weights: dict[str, float] | None = None
) -> dict[str, Any]:
    source_counts: defaultdict[str, int] = defaultdict(int)
    token_counts: defaultdict[str, int] = defaultdict(int)
    decision_counts: Counter[str] = Counter()
    capability_counts: Counter[str] = Counter()
    for record in records:
        source = str(record.get("source", record.get("metadata", {}).get("source", "unknown")))
        source_counts[source] += 1
        token_counts[source] += int(record.get("token_count", 0))
        behavior = record.get("behavior", record.get("metadata", {}).get("behavior", {}))
        if isinstance(behavior, dict):
            decision_counts[str(behavior.get("decision", "UNKNOWN"))] += 1
            capabilities = behavior.get("capabilities", [])
            if isinstance(capabilities, list):
                capability_counts.update(str(value) for value in capabilities)
    return {
        "sample_counts": dict(source_counts),
        "token_counts": dict(token_counts),
        "requested_weights": weights or {},
        "sample_share": _shares(source_counts),
        "token_share": _shares(token_counts),
        "decision_counts": dict(decision_counts),
        "decision_share": _shares(decision_counts),
        "capability_counts": dict(capability_counts),
        "capability_share": _shares(capability_counts),
    }


def _shares(values: dict[str, int] | Counter[str]) -> dict[str, float]:
    total = sum(values.values())
    return {key: value / total for key, value in values.items()} if total else {}


def structural_distributions(records: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    result: dict[str, Counter[str]] = {
        "turn_shape": Counter(),
        "tool_count": Counter(),
        "distractor_count": Counter(),
        "source": Counter(),
    }
    for record in records:
        metadata = record.get("metadata", record)
        messages = record.get("messages", [])
        result["turn_shape"]["multi_turn" if len(messages) > 3 else "single_turn"] += 1
        context = metadata.get("tool_context", {}) if isinstance(metadata, dict) else {}
        result["tool_count"][str(context.get("tool_count", len(record.get("tools", []))))] += 1
        result["distractor_count"][str(context.get("distractor_count", "unknown"))] += 1
        result["source"][str(record.get("source", metadata.get("source", "unknown")))] += 1
    return {key: dict(value) for key, value in result.items()}
