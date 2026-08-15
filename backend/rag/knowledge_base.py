import os
from typing import Any

import boto3
from dotenv import load_dotenv

load_dotenv()


class KnowledgeBase:

    def __init__(self):

        self.knowledge_base_id = os.getenv(
            "BEDROCK_KNOWLEDGE_BASE_ID"
        )

        self.client = boto3.client(
            "bedrock-agent-runtime",
            region_name=os.getenv(
                "AWS_REGION",
                "us-east-1"
            )
        )

    def retrieve(
        self,
        query: str,
        number_of_results: int = 5,
        metadata_filter: dict[str, Any] | None = None
    ) -> list[dict]:

        if not self.knowledge_base_id:

            return []

        vector_config: dict[str, Any] = {
            "numberOfResults": number_of_results
        }

        if metadata_filter:

            vector_config[
                "filter"
            ] = metadata_filter

        response = self.client.retrieve(

            knowledgeBaseId=(
                self.knowledge_base_id
            ),

            retrievalQuery={
                "text": query
            },

            retrievalConfiguration={
                "vectorSearchConfiguration":
                    vector_config
            }
        )

        results = []

        for item in response.get(
            "retrievalResults",
            []
        ):

            results.append(
                {
                    "text": item.get(
                        "content",
                        {}
                    ).get(
                        "text",
                        ""
                    ),

                    "score": item.get(
                        "score"
                    ),

                    "location": item.get(
                        "location",
                        {}
                    ),

                    "metadata": item.get(
                        "metadata",
                        {}
                    )
                }
            )

        return results