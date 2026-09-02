from dataclasses import dataclass


@dataclass(frozen=True)
class Run:
    run_id: str
    status: str
    parent_checkpoint: str | None = None
    result_checkpoint: str | None = None
    parent_run_id: str | None = None


def validate_lineage(runs: list[Run]) -> list[str]:
    ids = {r.run_id for r in runs}
    errors = []
    for r in runs:
        if r.parent_run_id and r.parent_run_id not in ids:
            errors.append(f"{r.run_id}: missing parent")
        if r.status in {"ACCEPTED", "FINAL"} and not r.result_checkpoint:
            errors.append(f"{r.run_id}: accepted run needs result checkpoint")
    return errors
