from dataclasses import dataclass, field
from typing import Any

from opengrad.data.behavior import validate_behavior

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
        behavior = self.metadata.get("behavior")
        if behavior is not None:
            if not isinstance(behavior, dict):
                raise TypeError("metadata.behavior must be an object")
            validate_behavior(
                behavior.get("decision", ""),
                behavior.get("capabilities", []),
                behavior.get("confidence", "known"),
            )
        tool_context = self.metadata.get("tool_context")
        if tool_context is not None:
            if not isinstance(tool_context, dict):
                raise TypeError("metadata.tool_context must be an object")
            for key in ("tool_count", "relevant_tool_count", "distractor_count"):
                if key in tool_context and (
                    not isinstance(tool_context[key], int) or tool_context[key] < 0
                ):
                    raise ValueError(f"{key} must be a non-negative integer")
        counterfactual = self.metadata.get("counterfactual")
        if counterfactual is not None:
            if not isinstance(counterfactual, dict) or not counterfactual.get("group_id"):
                raise ValueError("counterfactual requires group_id")
            if not counterfactual.get("variant") or not counterfactual.get("changed_factor"):
                raise ValueError("counterfactual requires variant and changed_factor")
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
