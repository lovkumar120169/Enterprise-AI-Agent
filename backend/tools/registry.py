from backend.tools.calculator import calculate
from backend.tools.stocks import get_stock
from backend.tools.weather import get_weather
from backend.tools.web_search import web_search
from backend.tools.knowledge_base import knowledge_base_tool

TOOL_FUNCTIONS = {
    "calculator": calculate,
    "weather": get_weather,
    "web_search": web_search,
    "stocks": get_stock,
    "knowledge_base": knowledge_base_tool.search
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
    },
    {
        "toolSpec": {
            "name": "knowledge_base",
            "description": (
                "Search the enterprise Knowledge Base "
                "for information contained in company "
                "documents. Use this tool when the user "
                "asks about information that may be available "
                "in the enterprise documents."
            ),
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": (
                                "The user's question or "
                                "search query for the "
                                "enterprise Knowledge Base."
                            )
                        }
                    },
                    "required": [
                        "query"
                    ]
                }
            }
        }
    }
]