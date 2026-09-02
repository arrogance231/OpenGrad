STAGES = ("BASELINE", "DATA_AUDIT", "SFT", "PREFERENCE")


def authorize(stage: str, state: dict[str, bool]) -> tuple[bool, str]:
    requirements = {
        "BASELINE": ["baseline_reproduced"],
        "DATA_AUDIT": ["baseline_accepted"],
        "SFT": ["baseline_accepted", "data_audit_complete"],
        "PREFERENCE": ["sft_fully_evaluated"],
    }
    missing = [x for x in requirements.get(stage, []) if not state.get(x, False)]
    return (not missing, "authorized" if not missing else "blocked: " + ", ".join(missing))
