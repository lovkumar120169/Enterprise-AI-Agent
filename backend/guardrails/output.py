import os

import boto3
from dotenv import load_dotenv

from backend.utils.logging import logger

load_dotenv()


class OutputGuardrail:

    def __init__(self):

        self.guardrail_id = os.getenv(
            "BEDROCK_GUARDRAIL_ID"
        )

        self.guardrail_version = os.getenv(
            "BEDROCK_GUARDRAIL_VERSION"
        )

        self.region = os.getenv(
            "AWS_REGION",
            "us-east-1"
        )

        self.client = boto3.client(
            "bedrock-runtime",
            region_name=self.region
        )

        logger.info(
            "OUTPUT GUARDRAIL INITIALIZED | "
            "configured=%s | version=%s | region=%s",
            bool(self.guardrail_id),
            self.guardrail_version,
            self.region
        )

    def check(self, text: str) -> dict:

        logger.info(
            "========== OUTPUT GUARDRAIL START =========="
        )

        if not self.guardrail_id:

            logger.error(
                "OUTPUT GUARDRAIL | "
                "Guardrail ID missing"
            )

            return {
                "allowed": False,
                "text": "",
                "reason": (
                    "Output Guardrail is not configured."
                )
            }

        try:

            logger.info(
                "OUTPUT GUARDRAIL → "
                "Amazon Bedrock ApplyGuardrail"
            )

            response = self.client.apply_guardrail(

                guardrailIdentifier=(
                    self.guardrail_id
                ),

                guardrailVersion=(
                    self.guardrail_version
                ),

                source="OUTPUT",

                content=[
                    {
                        "text": {
                            "text": text
                        }
                    }
                ]
            )

            action = response.get(
                "action",
                "UNKNOWN"
            )

            logger.info(
                "OUTPUT GUARDRAIL | "
                "AWS response | action=%s",
                action
            )

            if action == "GUARDRAIL_INTERVENED":

                logger.warning(
                    "OUTPUT GUARDRAIL | "
                    "RESPONSE BLOCKED"
                )

                return {
                    "allowed": False,
                    "text": (
                        "I can't provide that response."
                    ),
                    "reason": (
                        "Output blocked by Guardrail."
                    )
                }

            logger.info(
                "OUTPUT GUARDRAIL | "
                "RESPONSE PASSED"
            )

            logger.info(
                "========== OUTPUT GUARDRAIL END =========="
            )

            return {
                "allowed": True,
                "text": text,
                "reason": None
            }

        except Exception:

            logger.exception(
                "OUTPUT GUARDRAIL | "
                "ApplyGuardrail failed"
            )

            return {
                "allowed": False,
                "text": (
                    "I can't provide a response "
                    "right now."
                ),
                "reason": (
                    "Output safety service failed."
                )
            }