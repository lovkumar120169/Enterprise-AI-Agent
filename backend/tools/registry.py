from backend.tools.calculator import calculate
from backend.tools.weather import get_weather
from backend.tools.web_search import web_search
from backend.tools.stocks import get_stock


TOOL_FUNCTIONS = {

    "calculator": calculate,

    "weather": get_weather,

    "web_search": web_search,

    "stocks": get_stock
}


TOOL_DEFINITIONS = [

    {
        "toolSpec": {

            "name": "calculator",

            "description": (
                "Perform safe mathematical calculations."
            ),

            "inputSchema": {
                "json": {
                    "type": "object",

                    "properties": {

                        "expression": {
                            "type": "string"
                        }

                    },

                    "required": [
                        "expression"
                    ]
                }
            }
        }
    },

    {
        "toolSpec": {

            "name": "weather",

            "description": (
                "Get current weather information "
                "for a city."
            ),

            "inputSchema": {
                "json": {
                    "type": "object",

                    "properties": {

                        "city": {
                            "type": "string"
                        }

                    },

                    "required": [
                        "city"
                    ]
                }
            }
        }
    },

    {
        "toolSpec": {

            "name": "web_search",

            "description": (
                "Search the web for current "
                "information."
            ),

            "inputSchema": {
                "json": {

                    "type": "object",

                    "properties": {

                        "query": {
                            "type": "string"
                        }

                    },

                    "required": [
                        "query"
                    ]
                }
            }
        }
    },

    {
        "toolSpec": {

            "name": "stocks",

            "description": (
                "Get stock market information "
                "for a stock symbol."
            ),

            "inputSchema": {
                "json": {

                    "type": "object",

                    "properties": {

                        "symbol": {
                            "type": "string"
                        }

                    },

                    "required": [
                        "symbol"
                    ]
                }
            }
        }
    }
]