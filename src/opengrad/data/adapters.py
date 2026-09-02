from typing import Any

from opengrad.data.canonical import ToolConversation


def _messages(record: dict[str, Any]) -> list[dict[str, Any]]:
    messages = record.get("messages", record.get("conversation"))
    if not isinstance(messages, list):
        raise TypeError("missing messages/conversation list")
    return messages


def adapt(record: dict[str, Any], source: str, split: str = "fixture") -> ToolConversation:
    if not isinstance(record, dict) or not record.get("id"):
        raise ValueError("record id is required")
    messages = _messages(record)
    tools = record.get("tools", record.get("functions", []))
    if tools is None:
        tools = []
    c = ToolConversation(
        str(record["id"]),
        source,
        list(tools),
        messages,
        {
            "split": split,
            "source_revision": record.get("source_revision"),
            "contamination_status": "UNASSESSED",
            "source_fields": sorted(record),
        },
    )
    c.validate()
    return c


def adapt_xlam(record: dict[str, Any], split: str = "train") -> ToolConversation:
    return adapt(record, "xlam-function-calling-60k", split)


def adapt_when2call(record: dict[str, Any], split: str = "train_sft") -> ToolConversation:
    return adapt(record, "when2call", split)


def adapt_toolace(record: dict[str, Any], split: str = "train") -> ToolConversation:
    return adapt(record, "toolace", split)


def adapt_button(record: dict[str, Any], split: str = "train") -> ToolConversation:
    return adapt(record, "button", split)


def adapt_looptool(record: dict[str, Any], split: str = "train") -> ToolConversation:
    return adapt(record, "looptool-23k", split)


def adapt_glaive(record: dict[str, Any], split: str = "train") -> ToolConversation:
    return adapt(record, "glaive-function-calling-v2", split)
