import pytest

from opengrad.data.adapters import (
    adapt_button,
    adapt_glaive,
    adapt_looptool,
    adapt_toolace,
    adapt_when2call,
    adapt_xlam,
)


@pytest.mark.parametrize(
    "fn", [adapt_xlam, adapt_when2call, adapt_toolace, adapt_button, adapt_looptool, adapt_glaive]
)
def test_source_adapters_accept_documented_common_fixture(fn):
    result = fn(
        {
            "id": "fixture",
            "tools": [{"name": "lookup"}],
            "messages": [
                {"role": "user", "content": "find"},
                {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [{"id": "c1", "name": "lookup", "arguments": {"q": "x"}}],
                },
                {"role": "tool", "tool_call_id": "c1", "content": "ok"},
            ],
        }
    )
    assert result.metadata["source_fields"] == ["id", "messages", "tools"]


def test_adapter_rejects_missing_messages():
    with pytest.raises(TypeError):
        adapt_xlam({"id": "bad", "tools": []})


def test_adapter_preserves_unexpected_fields_in_provenance():
    result = adapt_glaive(
        {"id": "fixture", "messages": [{"role": "user", "content": "hi"}], "unexpected": True}
    )
    assert "unexpected" in result.metadata["source_fields"]
