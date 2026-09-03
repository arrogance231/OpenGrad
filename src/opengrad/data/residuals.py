from __future__ import annotations

from typing import Any

from opengrad.data.behavior import validate_weights

FAILURE_IDS = frozenset(
    {
        "UNDER_CALL",
        "OVER_CALL",
        "WRONG_TOOL",
        "INVALID_ARGUMENTS",
        "UNGROUNDED_ARGUMENTS",
        "MISSING_CLARIFICATION",
        "FALSE_UNSUPPORTED",
        "UNSUPPORTED_TOOL_CALL",
        "BAD_DEPENDENCY_ORDER",
        "BAD_PARALLELIZATION",
        "OBSERVATION_IGNORED",
        "PREMATURE_STOP",
        "FAILURE_RECOVERY_ERROR",
        "MULTI_TURN_STATE_ERROR",
        "FORMAT_ERROR",
    }
)

DEFAULT_MAPPING = {
    "UNDER_CALL": "must_call",
    "OVER_CALL": "must_not_call",
    "WRONG_TOOL": "near_match_distractor",
    "INVALID_ARGUMENTS": "argument_type_correctness",
    "UNGROUNDED_ARGUMENTS": "argument_grounding",
    "MISSING_CLARIFICATION": "clarify_before_call",
    "FALSE_UNSUPPORTED": "must_call",
    "UNSUPPORTED_TOOL_CALL": "unavailable_tool_rejection",
    "BAD_DEPENDENCY_ORDER": "dependency_ordering",
    "BAD_PARALLELIZATION": "parallel_calls",
    "OBSERVATION_IGNORED": "consume_tool_result",
    "PREMATURE_STOP": "followup_after_observation",
    "FAILURE_RECOVERY_ERROR": "tool_error_recovery",
    "MULTI_TURN_STATE_ERROR": "state_tracking",
    "FORMAT_ERROR": "argument_type_correctness",
}


def validate_residual_profile(profile: dict[str, Any]) -> None:
    for key in ("model", "baseline_experiment", "sample_count", "residuals"):
        if key not in profile:
            raise ValueError(f"residual profile requires {key}")
    if not isinstance(profile["sample_count"], int) or profile["sample_count"] < 1:
        raise ValueError("sample_count must be positive")
    unknown = set(profile["residuals"]) - FAILURE_IDS
    if unknown:
        raise ValueError(f"unknown failure ID: {sorted(unknown)}")
    if any(
        not isinstance(value, (int, float)) or value < 0 or value > 1
        for value in profile["residuals"].values()
    ):
        raise ValueError("residual rates must be between 0 and 1")


def residual_to_weights(
    profile: dict[str, Any],
    *,
    floors: dict[str, float] | None = None,
    caps: dict[str, float] | None = None,
    version: str = "residual-map-v1",
) -> dict[str, Any]:
    validate_residual_profile(profile)
    floors = floors or {}
    caps = caps or {}
    raw: dict[str, float] = {}
    for failure, rate in profile["residuals"].items():
        capability = DEFAULT_MAPPING[failure]
        raw[capability] = raw.get(capability, 0.0) + float(rate)
    for capability, value in floors.items():
        raw[capability] = max(raw.get(capability, 0.0), value)
    for capability, value in caps.items():
        raw[capability] = min(raw.get(capability, 0.0), value)
    total = sum(raw.values())
    weights = {key: value / total for key, value in raw.items()} if total else {}
    validate_weights(weights, set(weights))
    return {
        "algorithm_version": version,
        "baseline_experiment": profile["baseline_experiment"],
        "residual_profile_revision": profile.get("revision"),
        "target_weights": weights,
    }
