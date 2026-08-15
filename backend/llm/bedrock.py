import os
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv

from backend.reliability.retry import retry
from backend.utils.logging import logger

load_dotenv()


AWS_REGION = os.getenv(
    "AWS_REGION",
    "us-east-1"
)

MODEL_ID = os.getenv(
    "BEDROCK_MODEL_ID",
    "amazon.nova-lite-v1:0"
)


class BedrockClient:

    def __init__(self):

        self.client = boto3.client(
            "bedrock-runtime",
            region_name=AWS_REGION
        )

    @retry(
        max_attempts=2,
        delay_seconds=0.5
    )
    def converse(
        self,
        messages: list[dict[str, Any]],
        system_prompt: str,
        tools: list[dict[str, Any]] | None = None
    ) -> dict[str, Any]:

        request: dict[str, Any] = {
            "modelId": MODEL_ID,

            "system": [
                {
                    "text": system_prompt
                }
            ],

            "messages": messages,

            "inferenceConfig": {
                "maxTokens": 1024,
                "temperature": 0.3,
                "topP": 0.9
            }
        }

        if tools:

            request["toolConfig"] = {
                "tools": tools
            }

        try:

            logger.info(
                "Calling Bedrock model=%s",
                MODEL_ID
            )

            return self.client.converse(
                **request
            )

        except ClientError as error:

            error_data = error.response.get(
                "Error",
                {}
            )

            code = error_data.get(
                "Code",
                "Unknown"
            )

            message = error_data.get(
                "Message",
                str(error)
            )

            raise RuntimeError(
                f"Bedrock [{code}]: {message}"
            ) from error

        except BotoCoreError as error:

            raise RuntimeError(
                f"AWS SDK error: {error}"
            ) from error