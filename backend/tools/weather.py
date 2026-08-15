import os
import requests


OPENWEATHER_API_KEY = os.getenv(
    "OPENWEATHER_API_KEY"
)


def get_weather(
    city: str
) -> dict:

    if not OPENWEATHER_API_KEY:

        raise RuntimeError(
            "OPENWEATHER_API_KEY is not configured."
        )

    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        },
        timeout=5
    )

    response.raise_for_status()

    data = response.json()

    return {
        "city": city,
        "temperature_c": data[
            "main"
        ]["temp"],
        "feels_like_c": data[
            "main"
        ]["feels_like"],
        "humidity": data[
            "main"
        ]["humidity"],
        "description": data[
            "weather"
        ][0]["description"]
    }