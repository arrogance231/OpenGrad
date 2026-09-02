from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ToolConversation:
    """Source-independent conversation; renderers own model-native serialization."""

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
