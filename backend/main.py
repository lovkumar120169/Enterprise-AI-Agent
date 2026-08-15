from backend.agent.agent import AIAgent

agent = AIAgent()


def chat(
    user_message: str,
    history: list[dict] | None = None
) -> dict:

    if not user_message.strip():

        return {
            "success": False,
            "response": (
                "Please enter a message."
            ),
            "route": None,
            "iterations": 0,
            "tool_calls": [],
            "error": (
                "Empty user message."
            )
        }

    state = agent.run(
        user_message=user_message,
        history=history
    )

    return {
        "success": state.error is None,
        "response": state.response,
        "route": state.selected_tool,
        "iterations": state.iterations,
        "tool_calls": state.tool_calls,
        "blocked": state.blocked,
        "error": state.error
    }