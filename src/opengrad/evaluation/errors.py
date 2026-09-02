from typing import Any


def map_failure(*, code: str, detail: str, benchmark: str | None = None) -> dict[str, Any]:
    return {"taxonomy_code": code, "detail": detail, "benchmark": benchmark, "verified": False}


def map_predictions(predictions: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for p in predictions:
        code = p.get("error_code")
        if code:
            counts[code] = counts.get(code, 0) + 1
    return counts
