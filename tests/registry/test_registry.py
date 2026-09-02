from pathlib import Path

import yaml

from opengrad.registry.validate import validate


def test_registries_validate():
    assert validate(Path(__file__).parents[2]) == []


def test_dataset_metadata_is_field_level_and_clean_exclusion_is_preserved():
    root = Path(__file__).parents[2]
    records = yaml.safe_load((root / "registry/datasets.yaml").read_text())["datasets"]
    by_id = {record["id"]: record for record in records}
    assert by_id["xlam-function-calling-60k"]["sample_count"]["published"] == 60000
    assert by_id["xlam-function-calling-60k"]["license"]["verified"] is True
    assert by_id["xlam-function-calling-60k"]["processed_dataset_hash"]["status"] == (
        "pending_dataset_preparation"
    )
    assert by_id["apigen-mt-5k"]["contamination_status"] == "EXCLUDED_FROM_CLEAN_DEFAULT"
    assert "clean_default" in by_id["apigen-mt-5k"]["forbidden_splits"]
