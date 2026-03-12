from dotenv import load_dotenv
import json
from langchain_openai import ChatOpenAI

# Load environment variables (.env)
load_dotenv()

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# Supported categories
CATEGORIES = [
    "order_status",
    "delivery_delay",
    "refund_request",
    "product_issue",
    "subscription_issue",
    "payment_failure",
    "general_query",
    "other"
]

# Automation actions for each category
AUTOMATION_MAP = {
    "order_status": "Send tracking link automatically",
    "delivery_delay": "Send apology message and updated delivery ETA",
    "refund_request": "Initiate refund workflow",
    "product_issue": "Escalate to human support agent",
    "subscription_issue": "Provide subscription management link",
    "payment_failure": "Send payment retry link",
    "general_query": "Respond with FAQ information",
    "other": "Escalate to human support"
}


def classify_query(query: str):
    """
    Classify a customer support query into a category,
    detect sentiment, and determine automation action.
    """

    prompt = f"""
You are an AI customer support assistant.

Classify the customer message into one of these categories:
{CATEGORIES}

Also detect sentiment:
positive, neutral, angry

Return ONLY valid JSON in this format:

{{
"category": "",
"sentiment": "",
"confidence": 0.0
}}

Customer message:
{query}
"""

    response = llm.invoke(prompt)

    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        print("Warning: Model returned invalid JSON:", response.content)
        return {
            "query": query,
            "category": "other",
            "sentiment": "neutral",
            "confidence": 0.0,
            "automation_action": "Escalate to human"
        }

    category = result.get("category", "other")
    sentiment = result.get("sentiment", "neutral")
    confidence = result.get("confidence", 0.0)

    automation_action = AUTOMATION_MAP.get(category, "Escalate to human")

    return {
        "query": query,
        "category": category,
        "sentiment": sentiment,
        "confidence": confidence,
        "automation_action": automation_action
    }


# Local test
if __name__ == "__main__":

    test_query = "My order hasn't arrived yet and it's already 5 days late."

    result = classify_query(test_query)

    print("\nClassification Result\n")
    for key, value in result.items():
        print(f"{key}: {value}")