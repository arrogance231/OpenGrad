from pathlib import Path

import pyarrow.parquet as pq

from opengrad.data.materialize import materialize_parquet

FIXTURE = Path(__file__).parents[1] / "fixtures" / "raw" / "xlam" / "row.jsonl"


def test_materializer_writes_parquet_shards_and_resumes(tmp_path):
    import json

    source = tmp_path / "source.parquet"
    import pyarrow as pa

    row = json.loads(FIXTURE.read_text(encoding="utf-8").splitlines()[0])
    second = json.loads(json.dumps(row))
    second["id"] = "second"
    second["query"] = "Find a different city"
    pq.write_table(pa.Table.from_pylist([row, second]), source)
    output = tmp_path / "out"

    first = materialize_parquet(source, output, dataset="xlam", split="train", shard_size=1)
    assert first["manifest"]["shards"] == ["shard-000000.parquet", "shard-000001.parquet"]
    assert all((output / name).exists() for name in first["manifest"]["shards"])
    assert pq.read_table(output / "shard-000000.parquet").num_rows == 1

    second = materialize_parquet(source, output, dataset="xlam", split="train", shard_size=1)
    assert second["manifest"] == first["manifest"]


def test_materializer_rejects_corrupt_shard_and_rebuilds(tmp_path):
    import json

    import pyarrow as pa

    row = json.loads(FIXTURE.read_text(encoding="utf-8").splitlines()[0])
    source = tmp_path / "source.parquet"
    second = json.loads(json.dumps(row))
    second["id"] = "second"
    second["query"] = "Find a different city"
    pq.write_table(pa.Table.from_pylist([row, second]), source)
    output = tmp_path / "out"
    materialize_parquet(source, output, dataset="xlam", split="train", shard_size=1)
    (output / "shard-000001.parquet").write_bytes(b"corrupt")

    result = materialize_parquet(source, output, dataset="xlam", split="train", shard_size=1)
    assert result["manifest"]["counts"]["source_rows"] == 2
    assert pq.read_table(output / "shard-000001.parquet").num_rows == 1


def test_when2call_modes_keep_preference_and_evaluation_separate(tmp_path):
    import pyarrow as pa

    pref = tmp_path / "pref.parquet"
    pq.write_table(
        pa.Table.from_pylist(
            [
                {
                    "tools": [],
                    "messages": [{"role": "user", "content": "x"}],
                    "chosen_response": {"role": "assistant", "content": "yes"},
                    "rejected_response": {"role": "assistant", "content": "no"},
                }
            ]
        ),
        pref,
    )
    pref_result = materialize_parquet(
        pref, tmp_path / "pref-out", dataset="when2call", split="train_pref", mode="preference"
    )
    assert pref_result["manifest"]["mode"] == "preference"
    assert pq.read_table(tmp_path / "pref-out" / "shard-000000.parquet").column_names == [
        "example_id",
        "source",
        "tools",
        "context",
        "chosen",
        "rejected",
        "metadata",
    ]

    evaluation = tmp_path / "evaluation.parquet"
    pq.write_table(
        pa.Table.from_pylist(
            [
                {
                    "uuid": "e1",
                    "question": "Call?",
                    "correct_answer": "direct",
                    "answers": {"direct": "yes"},
                    "tools": [],
                }
            ]
        ),
        evaluation,
    )
    eval_result = materialize_parquet(
        evaluation, tmp_path / "eval-out", dataset="when2call", split="mcq", mode="evaluation"
    )
    assert eval_result["manifest"]["mode"] == "evaluation"
    assert pq.read_table(tmp_path / "eval-out" / "shard-000000.parquet").num_rows == 1
