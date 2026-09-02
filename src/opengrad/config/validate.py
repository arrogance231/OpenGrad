from typing import Any


def validate_config(
    config: dict[str, Any], known_models: set[str], clean: bool = True
) -> list[str]:
    errors = []
    if config.get("model_id") not in known_models:
        errors.append("unknown model ID")
    if not config.get("model_revision"):
        errors.append("base model revision must be pinned")
    if config.get("seed") is None:
        errors.append("seed is required")
    if config.get("training_stage") not in {"sft", "preference", "distillation", "rl"}:
        errors.append("invalid training stage")
    for ds in config.get("dataset_splits", []):
        if ds in {"when2call:test", "when2call:mcq", "when2call:llm_judge", "when2call:preference"}:
            errors.append("evaluation/preference split forbidden in SFT")
        if clean and ds == "Salesforce/APIGen-MT-5k":
            errors.append("APIGen-MT forbidden in clean experiment")
    if config.get("learning_rate", 1) > 1:
        errors.append("invalid learning rate")
    if config.get("precision") == "bf16" and config.get("hardware_type") == "cpu":
        errors.append("bf16 training requires explicit compatible accelerator")
    return errors
