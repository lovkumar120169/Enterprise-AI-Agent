from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentState:

    user_message: str

    conversation: list[dict[str, Any]] = field(
        default_factory=list
    )

    response: str = ""

    selected_tool: str | None = None

    use_knowledge_base: bool = False

    iterations: int = 0

    tool_calls: list[dict[str, Any]] = field(
        default_factory=list
    )

    citations: list[dict[str, Any]] = field(
        default_factory=list
    )

    error: str | None = None

    blocked: bool = False