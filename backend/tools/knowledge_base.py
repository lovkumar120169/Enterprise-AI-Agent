import os
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv

from backend.utils.logging import logger

load_dotenv()


class KnowledgeBaseTool:
    """
    Tool for retrieving relevant information from an
    Amazon Bedrock Managed Knowledge Base.

    This class ONLY performs retrieval.

    The ReAct agent remains responsible for sending the
    retrieved information back to the LLM and generating
    the final answer.
    """

    def __init__(self) -> None:

        self.region = os.getenv(
            "AWS_REGION",
            "us-east-1"
        )

        self.knowledge_base_id = os.getenv(
            "BEDROCK_KNOWLEDGE_BASE_ID"
        )

        self.number_of_results = int(
            os.getenv(
                "KNOWLEDGE_BASE_TOP_K",
                "5"
            )
        )

        self.client = boto3.client(
            "bedrock-agent-runtime",
            region_name=self.region
        )

        logger.info(
            "KNOWLEDGE BASE INITIALIZED | "
            "configured=%s | region=%s | top_k=%s",
            bool(self.knowledge_base_id),
            self.region,
            self.number_of_results
        )

    def search(
        self,
        query: str
    ) -> dict[str, Any]:
        """
        Search the Bedrock Managed Knowledge Base.

        Args:
            query: User's knowledge/document question.

        Returns:
            Dictionary containing retrieved chunks and
            source information.
        """

        logger.info(
            "KNOWLEDGE BASE | SEARCH START | query=%s",
            query
        )

        # --------------------------------------------------
        # Validate configuration
        # --------------------------------------------------

        if not self.knowledge_base_id:

            logger.error(
                "KNOWLEDGE BASE | "
                "BEDROCK_KNOWLEDGE_BASE_ID is missing"
            )

            return {
                "success": False,
                "error": (
                    "Knowledge Base is not configured."
                ),
                "results": []
            }

        # --------------------------------------------------
        # Validate query
        # --------------------------------------------------

        if not query or not query.strip():

            logger.warning(
                "KNOWLEDGE BASE | "
                "Empty query received"
            )

            return {
                "success": False,
                "error": (
                    "Knowledge Base query cannot be empty."
                ),
                "results": []
            }

        query = query.strip()

        # --------------------------------------------------
        # Protect the application from unreasonable values
        # --------------------------------------------------

        top_k = max(
            1,
            min(
                self.number_of_results,
                100
            )
        )

        try:

            logger.info(
                "KNOWLEDGE BASE | "
                "Calling Amazon Bedrock Retrieve"
            )

            # IMPORTANT:
            #
            # Your Knowledge Base is a MANAGED KB.
            #
            # Therefore we MUST use:
            #
            # managedSearchConfiguration
            #
            # and NOT:
            #
            # vectorSearchConfiguration
            #
            response = self.client.retrieve(

                knowledgeBaseId=(
                    self.knowledge_base_id
                ),

                retrievalQuery={
                    "text": query
                },

                retrievalConfiguration={
                    "managedSearchConfiguration": {
                        "numberOfResults": top_k
                    }
                }
            )

            raw_results = response.get(
                "retrievalResults",
                []
            )

            logger.info(
                "KNOWLEDGE BASE | "
                "Retrieved %s result(s)",
                len(raw_results)
            )

            results = []

            # --------------------------------------------------
            # Normalize AWS response
            # --------------------------------------------------

            for index, item in enumerate(
                raw_results,
                start=1
            ):

                content = item.get(
                    "content",
                    {}
                )

                text = content.get(
                    "text",
                    ""
                )

                score = item.get(
                    "score"
                )

                location = item.get(
                    "location",
                    {}
                )

                metadata = item.get(
                    "metadata",
                    {}
                )

                result = {
                    "rank": index,
                    "text": text,
                    "score": score,
                    "location": location,
                    "metadata": metadata
                }

                results.append(
                    result
                )

                logger.info(
                    "KNOWLEDGE BASE | "
                    "RESULT %s | score=%s",
                    index,
                    score
                )

            # --------------------------------------------------
            # No results
            # --------------------------------------------------

            if not results:

                logger.warning(
                    "KNOWLEDGE BASE | "
                    "No relevant documents found"
                )

                return {
                    "success": True,
                    "query": query,
                    "results": [],
                    "message": (
                        "No relevant information "
                        "was found in the knowledge base."
                    )
                }

            # --------------------------------------------------
            # Successful retrieval
            # --------------------------------------------------

            logger.info(
                "KNOWLEDGE BASE | "
                "SEARCH COMPLETE | results=%s",
                len(results)
            )

            return {
                "success": True,
                "query": query,
                "results": results
            }

        except (ClientError, BotoCoreError) as error:

            logger.exception(
                "KNOWLEDGE BASE | AWS ERROR"
            )

            return {
                "success": False,
                "query": query,
                "results": [],
                "error": (
                    "Knowledge Base service "
                    "request failed."
                ),
                "details": str(error)
            }

        except Exception as error:

            logger.exception(
                "KNOWLEDGE BASE | "
                "UNEXPECTED ERROR"
            )

            return {
                "success": False,
                "query": query,
                "results": [],
                "error": (
                    "Unexpected Knowledge Base error."
                ),
                "details": str(error)
            }


# ----------------------------------------------------------
# Singleton instance
# ----------------------------------------------------------

knowledge_base_tool = KnowledgeBaseTool()