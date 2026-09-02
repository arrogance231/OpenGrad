from opengrad.config.validate import validate_config


def test_clean_sft_rejects_eval_and_contaminated_sources():
    errors = validate_config(
        {
            "model_id": "qwen3.5-2b",
            "model_revision": "rev",
            "seed": 1,
            "training_stage": "sft",
            "dataset_splits": ["when2call:mcq", "Salesforce/APIGen-MT-5k"],
        },
        {"qwen3.5-2b"},
    )
    assert any("evaluation" in e for e in errors) and any("APIGen-MT" in e for e in errors)


def test_stage_config_rejects_missing_pins_and_invalid_learning_rate():
    errors = validate_config(
        {"model_id": "unknown", "training_stage": "bad", "learning_rate": 2}, {"qwen3.5-2b"}
    )
    assert len(errors) >= 4
