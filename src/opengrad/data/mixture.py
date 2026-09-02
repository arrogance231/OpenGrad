from collections import defaultdict
from typing import Any


def analyze(
    records: list[dict[str, Any]], weights: dict[str, float] | None = None
) -> dict[str, Any]:
    sample_counts: defaultdict[str, int] = defaultdict(int)
    token_counts: defaultdict[str, int] = defaultdict(int)
    for record in records:
        source = str(record.get("source", "unknown"))
        sample_counts[source] += 1
        token_counts[source] += int(record.get("token_count", 0))
    return {
        "sample_counts": dict(sample_counts),
        "token_counts": dict(token_counts),
        "requested_weights": weights or {},
        "sample_share": _shares(sample_counts),
        "token_share": _shares(token_counts),
    }


def _shares(values: dict[str, int]) -> dict[str, float]:
    total = sum(values.values())
    return {key: value / total for key, value in values.items()} if total else {}
