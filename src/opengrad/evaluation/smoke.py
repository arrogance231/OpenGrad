from pathlib import Path
from typing import Any

from opengrad.evaluation.schema import validate_result


def run_smoke(benchmark: str, destination: Path) -> dict[str, Any]:
    result = {
        "run_id": "SMOKE_TEST_ONLY/fixture",
        "checkpoint_id": "SMOKE_TEST_ONLY",
        "benchmark": benchmark,
        "benchmark_revision": "fixture",
        "evaluator_revision": "fixture",
        "model_adapter": "deterministic-mock",
        "generation_config": {},
        "seed": 0,
        "metrics": {"smoke_cases": 1},
        "category_metrics": {},
        "errors": {},
        "raw_predictions_path": "SMOKE_TEST_ONLY",
        "timestamp": "SMOKE_TEST_ONLY",
    }
    validate_result(result)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(__import__("json").dumps(result, indent=2) + "\n")
    return result
