from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from opengrad.data.stats import analyze, structural_distributions


def load_records(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    if text.startswith("["):
        value = json.loads(text)
        if not isinstance(value, list):
            raise ValueError("records JSON must be an array")
        return value
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def coverage_report(records: list[dict[str, Any]]) -> dict[str, Any]:
    result = analyze(records)
    result["structural"] = structural_distributions(records)
    result["total_examples"] = len(records)
    return result


def render_human(report: dict[str, Any]) -> str:
    lines = [f"Total examples: {report['total_examples']}", "", "Decision policy:"]
    decisions = report.get("decision_counts", {})
    total = report["total_examples"] or 1
    for key in ("CALL", "ANSWER", "CLARIFY", "UNSUPPORTED", "UNKNOWN"):
        if key in decisions:
            lines.append(f"  {key:<12} {decisions[key] / total:.1%} ({decisions[key]})")
    lines.append("\nCapabilities:")
    for key, count in sorted(report.get("capability_counts", {}).items()):
        lines.append(f"  {key:<30} {count / total:.1%} ({count})")
    lines.append("\nStructural distributions:")
    for category, values in report.get("structural", {}).items():
        lines.append(f"  {category}: {values}")
    return "\n".join(lines)
