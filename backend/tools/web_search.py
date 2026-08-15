import os
import requests


TAVILY_API_KEY = os.getenv(
    "TAVILY_API_KEY"
)


def web_search(
    query: str,
    max_results: int = 5
) -> dict:

    if not TAVILY_API_KEY:

        raise RuntimeError(
            "TAVILY_API_KEY is not configured."
        )

    response = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": TAVILY_API_KEY,
            "query": query,
            "max_results": max_results
        },
        timeout=8
    )

    response.raise_for_status()

    data = response.json()

    results = []

    for item in data.get(
        "results",
        []
    ):

        results.append(
            {
                "title": item.get(
                    "title",
                    ""
                ),
                "url": item.get(
                    "url",
                    ""
                ),
                "content": item.get(
                    "content",
                    ""
                )
            }
        )

    return {
        "query": query,
        "results": results
    }