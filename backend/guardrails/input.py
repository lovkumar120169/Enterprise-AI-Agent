import os

import boto3
from dotenv import load_dotenv

from backend.utils.logging import logger


load_dotenv()


class InputGuardrail:

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
            "INPUT GUARDRAIL INITIALIZED | "
            "configured=%s | version=%s | region=%s",
            bool(self.guardrail_id),
            self.guardrail_version,
            self.region
        )

    def check(self, text: str) -> dict:

        logger.info(
            "========== INPUT GUARDRAIL START =========="
        )

        logger.info(
            "INPUT GUARDRAIL | checking user request"
        )

        if not self.guardrail_id:

            logger.error(
                "INPUT GUARDRAIL | "
                "Guardrail ID is missing"
            )

            return {
                "allowed": False,
                "text": "",
                "reason": (
                    "Input Guardrail is not configured."
                )
            }

        if not self.guardrail_version:

            logger.error(
                "INPUT GUARDRAIL | "
                "Guardrail version is missing"
            )

            return {
                "allowed": False,
                "text": "",
                "reason": (
                    "Input Guardrail version is missing."
                )
            }

        try:

            logger.info(
                "INPUT GUARDRAIL | "
                "calling Amazon Bedrock ApplyGuardrail"
            )

            response = self.client.apply_guardrail(

                guardrailIdentifier=(
                    self.guardrail_id
                ),

                guardrailVersion=(
                    self.guardrail_version
                ),

                source="INPUT",

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
                "INPUT GUARDRAIL | "
                "AWS response received | action=%s",
                action
            )

            if action == "GUARDRAIL_INTERVENED":

                logger.warning(
                    "INPUT GUARDRAIL | "
                    "REQUEST BLOCKED"
                )

                logger.info(
                    "========== INPUT GUARDRAIL END | BLOCKED =========="
                )

                return {
                    "allowed": False,
                    "text": "",
                    "reason": (
                        "Request blocked by "
                        "Amazon Bedrock Guardrail."
                    )
                }

            logger.info(
                "INPUT GUARDRAIL | "
                "REQUEST PASSED"
            )

            logger.info(
                "========== INPUT GUARDRAIL END | PASSED =========="
            )

            return {
                "allowed": True,
                "text": text,
                "reason": None
            }

        except Exception as error:

            logger.exception(
                "INPUT GUARDRAIL | "
                "ApplyGuardrail failed"
            )

            return {
                "allowed": False,
                "text": "",
                "reason": (
                    "Input safety service "
                    "is unavailable."
                )
            }