from pathlib import Path

from opengrad.data.audit import coverage_report, load_records, render_human


def test_behavior_coverage_report_is_measured_from_records():
    records = load_records(Path("tests/fixtures/tool_use_behavior.jsonl"))
    report = coverage_report(records)
    assert report["total_examples"] == 4
    assert report["decision_counts"] == {"CALL": 1, "ANSWER": 1, "CLARIFY": 1, "UNSUPPORTED": 1}
    assert report["structural"]["tool_count"]["1"] == 4
    assert "CALL" in render_human(report)
