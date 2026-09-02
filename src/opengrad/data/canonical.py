from dataclasses import dataclass, field
from typing import Any

ROLES = {"system", "user", "assistant", "tool"}


@dataclass(frozen=True)
class ToolConversation:
    id: str
    source: str
    tools: list[dict[str, Any]]
    messages: list[dict[str, Any]]
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.id or not self.source:
            raise ValueError("id and source are required")
        if not isinstance(self.tools, list) or not isinstance(self.messages, list):
            raise TypeError("tools and messages must be lists")
        if not self.metadata.get("split"):
            raise ValueError("metadata.split is required for provenance")
        tool_names = set()
        for tool in self.tools:
            if not isinstance(tool, dict) or not isinstance(tool.get("name"), str):
                raise TypeError("each tool needs a name")
            if tool["name"] in tool_names:
                raise ValueError("duplicate tool name")
            tool_names.add(tool["name"])
        seen_calls = set()
        for index, message in enumerate(self.messages):
            if not isinstance(message, dict) or message.get("role") not in ROLES:
                raise ValueError(f"message {index} has invalid role")
            role = message["role"]
            if role in {"system", "user", "assistant"} and "content" not in message:
                raise ValueError(f"message {index} needs content")
            if role == "assistant":
                calls = message.get("tool_calls", [])
                if not isinstance(calls, list):
                    raise ValueError("tool_calls must be a list")
                for call in calls:
                    if not isinstance(call, dict) or not isinstance(call.get("name"), str):
                        raise TypeError("tool call needs name")
                    if call["name"] not in tool_names:
                        raise ValueError(f"unknown tool: {call['name']}")
                    if not isinstance(call.get("arguments", {}), dict):
                        raise TypeError("tool arguments must be an object")
                    call_id = call.get("id")
                    if call_id:
                        if call_id in seen_calls:
                            raise ValueError("duplicate tool call id")
                        seen_calls.add(call_id)
            if role == "tool" and not isinstance(message.get("tool_call_id"), str):
                raise ValueError("tool message needs tool_call_id")


def canonical_dict(c: ToolConversation) -> dict[str, Any]:
    c.validate()
    return {
        "id": c.id,
        "source": c.source,
        "tools": c.tools,
        "messages": c.messages,
        "metadata": c.metadata,
    }
