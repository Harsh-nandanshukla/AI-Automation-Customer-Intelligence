from dotenv import load_dotenv
import json
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

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


def classify_query(query):

    prompt = f"""
You are an AI customer support assistant.

Below are examples of how customer queries should be classified.

Example 1
Message: Order shows delivered but I never received it.
Category: order_status
Sentiment: angry
Confidence: 0.91

Example 2
Message: I was charged twice for the same order.
Category: payment_failure
Sentiment: angry
Confidence: 0.92

Example 3
Message: My package has been stuck in the warehouse for several days.
Category: delivery_delay
Sentiment: frustrated
Confidence: 0.90

Now classify the following customer message.

Valid categories:
{CATEGORIES}

Sentiment options:
positive, neutral, angry

Also generate a short helpful customer support reply appropriate for the issue.

Return ONLY valid JSON.
Do not include explanations, markdown, or text outside the JSON object.

Return JSON in this exact format:

{{
"category": "",
"sentiment": "",
"confidence": 0.0,
"suggested_reply": ""
}}

Customer message:
{query}

"""

    response = llm.invoke(prompt)

    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        return {
            "query": query,
            "category": "other",
            "sentiment": "neutral",
            "confidence": 0.0,
            "suggested_reply": "Thank you for contacting support. Our team will assist you shortly.",
            "automation_action": "Escalate to human"
        }

    category = result.get("category", "other")
    sentiment = result.get("sentiment", "neutral")
    confidence = result.get("confidence", 0.0)
    # Priority assignment based on sentiment
    priority = (
    "high" if sentiment == "angry"
    else "medium" if sentiment == "neutral"
    else "low"
    )

    suggested_reply = result.get(
        "suggested_reply",
        "Thank you for contacting support. Our team will assist you shortly."
    )

    automation_action = AUTOMATION_MAP.get(category, "Escalate to human")

    # Confidence-based escalation gate
    if confidence < 0.80:
         automation_action = "Escalate to human support (low confidence)"

      
    return {
        "query": query,
        "category": category,
        "sentiment": sentiment,
        "priority": priority,
        "confidence": confidence,
        "suggested_reply": suggested_reply,
        "automation_action": automation_action
    }


if __name__ == "__main__":

    test_query = "My order hasn't arrived yet and it's already 5 days late."

    result = classify_query(test_query)

    print("\nClassification Result\n")

    for k, v in result.items():
        print(f"{k}: {v}")