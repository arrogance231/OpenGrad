import pytest

from opengrad.data.canonical import ToolConversation


def test_canonical_supports_parallel_calls_and_results():
    c = ToolConversation(
        "x",
        "fixture",
        [{"name": "a"}, {"name": "b"}],
        [
            {"role": "system", "content": "tools"},
            {"role": "user", "content": "go"},
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {"id": "1", "name": "a", "arguments": {}},
                    {"id": "2", "name": "b", "arguments": {}},
                ],
            },
            {"role": "tool", "tool_call_id": "1", "content": "a"},
            {"role": "tool", "tool_call_id": "2", "content": "b"},
        ],
        {"split": "dev"},
    )
    c.validate()


def test_canonical_rejects_unknown_tool():
    c = ToolConversation(
        "x",
        "fixture",
        [{"name": "a"}],
        [
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [{"name": "missing", "arguments": {}}],
            }
        ],
        {"split": "dev"},
    )
    with pytest.raises(ValueError, match="unknown tool"):
        c.validate()
