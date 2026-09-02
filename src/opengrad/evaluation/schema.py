from typing import Any


def validate_result(result: dict[str, Any]) -> None:
    required = (
        "run_id",
        "checkpoint_id",
        "benchmark",
        "benchmark_revision",
        "evaluator_revision",
        "model_adapter",
        "generation_config",
        "metrics",
        "errors",
        "raw_predictions_path",
        "timestamp",
    )
    missing = [k for k in required if k not in result]
    if missing:
        raise ValueError("missing result fields: " + ", ".join(missing))
    if result["timestamp"] and not isinstance(result["timestamp"], str):
        raise TypeError("timestamp must be ISO string")
    for key in ("metrics", "category_metrics", "errors"):
        if key in result and not isinstance(result[key], dict):
            raise TypeError(f"{key} must be object")
