def route_request(user_message: str) -> str:
    """
    Temporary router.

    Later this will use an LLM-based decision process
    to select tools such as weather, calculator,
    web search, stocks, or general LLM.
    """

    return "llm"