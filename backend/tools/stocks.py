import os
import requests


ALPHA_VANTAGE_API_KEY = os.getenv(
    "ALPHA_VANTAGE_API_KEY"
)


def get_stock(
    symbol: str
) -> dict:

    if not ALPHA_VANTAGE_API_KEY:

        raise RuntimeError(
            "ALPHA_VANTAGE_API_KEY "
            "is not configured."
        )

    response = requests.get(
        "https://www.alphavantage.co/query",
        params={
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": ALPHA_VANTAGE_API_KEY
        },
        timeout=8
    )

    response.raise_for_status()

    data = response.json()

    quote = data.get(
        "Global Quote"
    )

    if not quote:

        raise RuntimeError(
            f"No stock data found for {symbol}."
        )

    return {
        "symbol": quote.get(
            "01. symbol"
        ),
        "price": quote.get(
            "05. price"
        ),
        "change": quote.get(
            "09. change"
        ),
        "change_percent": quote.get(
            "10. change percent"
        )
    }