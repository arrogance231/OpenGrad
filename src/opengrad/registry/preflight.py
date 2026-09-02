from pathlib import Path

from opengrad.registry.validate import validate


def check(root: Path) -> dict[str, bool]:
    return {
        "Repository": (root / ".git").exists(),
        "Registries": not validate(root),
        "Dataset policies": (root / "configs/data/tool_calling/contamination.yaml").exists(),
        "Experiment lineage": (root / "src/opengrad/experiments/lineage.py").exists(),
        "Benchmark harnesses": (root / "src/opengrad/evaluation/smoke.py").exists(),
        "Contamination tooling": (root / "src/opengrad/contamination/scanner.py").exists(),
        "Reporting": (root / "src/opengrad/reporting/generate.py").exists(),
    }
