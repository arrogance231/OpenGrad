import json
from pathlib import Path

from opengrad.data.real_analysis import analyze_corpus, build_clean_sft_index, lineage_status


def row(example_id, source="a", decision="CALL", split="train", contamination="UNASSESSED"):
    return {
        "id": example_id,
        "source": source,
        "tools": [{"name": "lookup"}],
        "messages": [{"role": "user", "content": "same"}],
        "metadata": {
            "split": split,
            "contamination_status": contamination,
            "behavior": {"decision": decision, "capabilities": ["must_call"]},
        },
        "canonical_hash": f"canonical-{example_id}",
    }


def test_real_analysis_reports_measured_overlap_coverage_and_source_quality():
    result = analyze_corpus({"a": [row("1", "a"), row("2", "a", "ANSWER")], "b": [row("3", "b")]})
    assert result["status"] == "MEASURED"
    assert result["overlap"]["a__b"]["user_prompt"] == 1
    assert result["behavioral_coverage"]["decision_counts"] == {"CALL": 2, "ANSWER": 1}
    assert result["source_quality"]["a"]["status"] == "MEASURED"


def test_clean_sft_index_does_not_call_unassessed_rows_clean():
    result = build_clean_sft_index(
        [row("1", contamination="CLEAN"), row("2"), row("3", split="mcq")]
    )
    assert result["status"] == "BLOCKED"
    assert result["clean_candidate_ids"] == ["1"]
    assert "2" in result["blocked_ids"]


def test_lineage_is_blocked_without_rendered_and_token_manifests(tmp_path: Path):
    result = lineage_status(tmp_path / "missing.json", tmp_path / "missing.tokens.json")
    assert result == {
        "status": "BLOCKED",
        "reasons": ["render_manifest_missing", "token_manifest_missing"],
    }


def test_analysis_is_machine_readable(tmp_path: Path):
    path = tmp_path / "rows.jsonl"
    path.write_text(json.dumps(row("1")) + "\n", encoding="utf-8")
    result = analyze_corpus({"a": path})
    assert result["groups"]["a"]["records"] == 1


def test_overlap_does_not_count_missing_fingerprints_as_matches():
    result = analyze_corpus({"a": [row("1")], "b": [row("2")]})
    assert result["overlap"]["a__b"]["raw_hash"] == 0
