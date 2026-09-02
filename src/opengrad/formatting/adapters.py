from typing import Any

from opengrad.data.canonical import ToolConversation


def from_source(
    record: dict[str, Any], *, source: str, split: str, revision: str | None = None
) -> ToolConversation:
    """Minimal adapter boundary; production adapters must be source-specific and audited."""
    conversation = ToolConversation(
        id=str(record["id"]),
        source=source,
        tools=list(record.get("tools", [])),
        messages=list(record.get("messages", [])),
        metadata={
            "split": split,
            "source_revision": revision,
            "contamination_status": "UNASSESSED",
        },
    )
    conversation.validate()
    return conversation


class ModelRenderer:
    """Interface marker for future native chat/tool protocol renderers."""

    def render(self, conversation: ToolConversation) -> list[dict[str, Any]]:
        raise NotImplementedError
