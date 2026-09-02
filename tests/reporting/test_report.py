from opengrad.reporting.generate import generate_report


def test_report_marks_synthetic_data(tmp_path):
    out = generate_report("fixture", {"metric": 0.5}, tmp_path / "report.md")
    assert "SYNTHETIC TEST DATA" in out.read_text()
