from pathlib import Path
from typing import Any


def generate_report(kind: str, record: dict[str, Any], destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {kind} report", "", "**SYNTHETIC TEST DATA — NOT A RESEARCH RESULT**", ""]
    for key, value in record.items():
        lines.append(f"- **{key}:** {value}")
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return destination
