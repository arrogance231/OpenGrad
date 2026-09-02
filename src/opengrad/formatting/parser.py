import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ParsedCall:
    name: str
    arguments: dict[str, Any]
    call_id: str | None = None
    state: str = "RAW_VALID"


def parse_calls(value: Any) -> list[ParsedCall]:
    if not isinstance(value, list):
        value = [value]
    result = []
    for item in value:
        if isinstance(item, str):
            try:
                item = json.loads(item)
            except json.JSONDecodeError as exc:
                raise ValueError("INVALID: malformed JSON") from exc
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            raise TypeError("INVALID: missing call name")
        args = item.get("arguments", {})
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except json.JSONDecodeError as exc:
                raise ValueError("INVALID: malformed arguments") from exc
        if not isinstance(args, dict):
            raise TypeError("INVALID: arguments must be object")
        result.append(ParsedCall(item["name"], args, item.get("id"), "RAW_VALID"))
    return result
