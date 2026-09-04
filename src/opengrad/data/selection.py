from collections import Counter
from typing import Any


def validate_counterfactual_groups(records: list[dict[str, Any]]) -> None:
    groups: Counter[str] = Counter()
    for record in records:
        metadata = record.get("metadata", record)
        counterfactual = metadata.get("counterfactual", {}) if isinstance(metadata, dict) else {}
        if counterfactual:
            groups[str(counterfactual.get("group_id"))] += 1
    invalid = sorted(group for group, count in groups.items() if count < 2)
    if invalid:
        raise ValueError(f"counterfactual groups require at least two members: {invalid}")


def validate_sft_selection(
    splits: list[str], contamination_sources: set[str] | None = None
) -> None:
    forbidden = {"when2call:test", "when2call:mcq", "when2call:llm_judge", "when2call:preference"}
    if forbidden.intersection(splits):
        raise ValueError("evaluation/preference split forbidden in SFT")
    if contamination_sources and any(source in contamination_sources for source in splits):
        raise ValueError("contaminated source forbidden in clean SFT")


def validate_training_records(records: list[dict[str, Any]]) -> None:
    forbidden = {"preference_only", "evaluation_only", "contaminated"}
    violations = [
        record.get("id", "unknown")
        for record in records
        if record.get("metadata", {}).get("eligibility") in forbidden
        or record.get("metadata", {}).get("contamination_status")
        not in {None, "UNASSESSED", "CLEAN"}
    ]
    if violations:
        raise ValueError(f"records forbidden from clean training: {violations}")
