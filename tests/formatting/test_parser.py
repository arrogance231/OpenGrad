import pytest

from opengrad.formatting.parser import parse_calls


def test_parser_handles_nested_unicode_and_multiple_calls():
    calls = parse_calls(
        [
            '{"name":"a","arguments":{"x":[1,{"u":"\u2603"}]},"id":"1"}',
            {"name": "b", "arguments": {}},
        ]
    )
    assert calls[0].arguments["x"][1]["u"] == "☃" and len(calls) == 2


@pytest.mark.parametrize(
    "value", ['{"name":"a","arguments":', {"arguments": {}}, {"name": "a", "arguments": []}]
)
def test_parser_marks_invalid_without_repair(value):
    with pytest.raises((ValueError, TypeError), match="INVALID"):
        parse_calls(value)
