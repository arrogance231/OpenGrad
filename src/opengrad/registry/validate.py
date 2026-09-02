import json
from pathlib import Path
from typing import Any


def load_yaml(path: Path) -> Any:
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError as exc:
        raise RuntimeError("Install the dev extra for YAML validation") from exc
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate(root: Path) -> list[str]:
    errors = []
    for name in (
        "datasets.yaml",
        "benchmarks.yaml",
        "models.yaml",
        "runtimes.yaml",
        "hardware.yaml",
    ):
        try:
            value = load_yaml(root / "registry" / name)
            if not isinstance(value, dict) or "schema_version" not in value:
                errors.append(name + ": missing schema_version")
        except (ImportError, OSError, TypeError, ValueError) as exc:
            errors.append(f"{name}: {exc}")
    try:
        schema = json.loads((root / "registry/experiments.schema.json").read_text())
        if schema.get("$schema") is None:
            errors.append("experiments.schema.json: missing $schema")
    except (OSError, TypeError, ValueError) as exc:
        errors.append(f"experiments.schema.json: {exc}")
    return errors


def main() -> int:
    errors = validate(Path.cwd())
    print("registry validation: OK" if not errors else "\n".join(errors))
    return int(bool(errors))
