from pathlib import Path

from opengrad.evaluation.errors import map_predictions
from opengrad.evaluation.schema import validate_result
from opengrad.evaluation.smoke import run_smoke


def test_smoke_result_is_explicit(tmp_path: Path):
    result = run_smoke("fixture-benchmark", tmp_path / "result.json")
    validate_result(result)
    assert result["run_id"].startswith("SMOKE_TEST_ONLY")


def test_error_mapping_is_taxonomy_agnostic():
    assert map_predictions(
        [{"error_code": "E10"}, {"error_code": "E10"}, {"error_code": "E03"}]
    ) == {"E10": 2, "E03": 1}
