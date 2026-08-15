import os

import boto3
from dotenv import load_dotenv


load_dotenv()


AWS_REGION = os.getenv(
    "AWS_REGION",
    "us-east-1"
)

KNOWLEDGE_BASE_ID = os.getenv(
    "BEDROCK_KNOWLEDGE_BASE_ID"
)


print("================================")
print("KNOWLEDGE BASE TEST")
print("================================")

print(
    "Region:",
    AWS_REGION
)

print(
    "Knowledge Base ID:",
    KNOWLEDGE_BASE_ID
)

print("================================")


if not KNOWLEDGE_BASE_ID:

    raise RuntimeError(
        "BEDROCK_KNOWLEDGE_BASE_ID "
        "is not configured."
    )


client = boto3.client(
    "bedrock-agent-runtime",
    region_name=AWS_REGION
)


query = (
    "When was Acme Technologies founded?"
)


print()
print("Query:")
print(query)
print()


try:

    response = client.retrieve(

        knowledgeBaseId=(
            KNOWLEDGE_BASE_ID
        ),

        retrievalQuery={
            "text": query
        },

        retrievalConfiguration={
            "managedSearchConfiguration": {
                "numberOfResults": 5
            }
        }
    )

    results = response.get(
        "retrievalResults",
        []
    )

    print(
        f"Retrieved {len(results)} results."
    )

    print()

    for index, result in enumerate(
        results,
        start=1
    ):

        print(
            f"========== RESULT {index} =========="
        )

        print(
            "Score:",
            result.get("score")
        )

        content = result.get(
            "content",
            {}
        )

        print(
            "Text:"
        )

        print(
            content.get(
                "text",
                ""
            )
        )

        print()

        print(
            "Location:"
        )

        print(
            result.get(
                "location",
                {}
            )
        )

        print()

except Exception as error:

    print()
    print(
        "KNOWLEDGE BASE TEST FAILED"
    )

    print()

    print(
        type(error).__name__
    )

    print(
        str(error)
    )