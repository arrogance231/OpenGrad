from typing import Any

from opengrad.data.canonical import ToolConversation


def from_source(
    record: dict[str, Any], *, source: str, split: str, revision: str | None = None
) -> ToolConversation:
    conversation = ToolConversation(
        str(record["id"]),
        source,
        list(record.get("tools", [])),
        list(record.get("messages", [])),
        {"split": split, "source_revision": revision, "contamination_status": "UNASSESSED"},
    )
    conversation.validate()
    return conversation


class ModelRenderer:
    status = "REQUIRES_RUNTIME_VALIDATION"

    def render(self, conversation: ToolConversation) -> list[dict[str, Any]]:
        raise NotImplementedError


class FixtureRenderer(ModelRenderer):
    def __init__(self, family: str):
        self.family = family

    def render(self, conversation: ToolConversation) -> list[dict[str, Any]]:
        conversation.validate()
        return conversation.messages


RENDERERS = {family: FixtureRenderer(family) for family in ("qwen", "lfm", "gemma", "llama", "phi")}
