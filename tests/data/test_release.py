from pathlib import Path

from opengrad.data.release import _parquet_row, validate_release


def test_release_row_preserves_source_lineage():
    row = {
        "id": "og-1",
        "schema_version": "tool_use_ir_v1",
        "canonical_hash": "hash",
        "tools": [],
        "messages": [],
        "metadata": {
            "split": "train",
            "adapter": "fixture",
            "adapter_version": "1.0.0",
            "source": {"upstream_id": "source-1"},
            "behavior": {"decision": "ANSWER", "confidence": "known", "capabilities": []},
        },
    }
    result = _parquet_row(row, {"id": "fixture", "source_revision": "rev"})
    assert result["opengrad_id"] == "og-1"
    assert result["source_record_id"] == "source-1"
    assert result["source_revision"] == "rev"
    assert result["behavior_decision"] == "ANSWER"


def test_release_validator_fails_closed_without_manifest(tmp_path: Path):
    assert validate_release(tmp_path) == ["release-manifest.json missing"]
