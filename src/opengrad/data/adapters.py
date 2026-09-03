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
    metadata = {
        "split": split,
        "source": {
            "dataset_id": source,
            "revision": record.get("source_revision"),
            "original_split": record.get("original_split", split),
        },
        "source_revision": record.get("source_revision"),
        "contamination_status": record.get("contamination_status", "UNASSESSED"),
        "source_fields": sorted(record),
    }
    for key in ("behavior", "tool_context", "interaction", "training", "counterfactual"):
        if key in record:
            metadata[key] = record[key]
    if "tool_context" not in metadata:
        metadata["tool_context"] = {"tool_count": len(tools)}
        for key in ("relevant_tool_count", "distractor_count"):
            if record.get(key) is not None:
                metadata["tool_context"][key] = record[key]
    c = ToolConversation(
        str(record["id"]),
        source,
        list(tools),
        messages,
        metadata,
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
