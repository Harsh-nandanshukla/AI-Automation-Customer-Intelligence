import pandas as pd
import time
from classifier import classify_query

INPUT_FILE = "sample_queries.csv"
OUTPUT_FILE = "results.csv"


def run_batch():

    print("Loading dataset...")

    df = pd.read_csv(INPUT_FILE)

    results = []

    total = len(df)

    for i, row in df.iterrows():

        query = row["query"]

        print(f"Processing {i+1}/{total}: {query[:50]}...")

        try:

            result = classify_query(query)

            results.append({
                "id": row["id"],
                "query": query,
                "expected_category": row["expected_category"],
                "predicted_category": result["category"],
                "sentiment": result["sentiment"],
                "priority": result["priority"],
                "confidence": result["confidence"],
                "suggested_reply": result["suggested_reply"],
                "automation_action": result["automation_action"]
            })

        except Exception as e:

            print(f"Error on query {i+1}: {e}")

            results.append({
                "id": row["id"],
                "query": query,
                "expected_category": row["expected_category"],
                "predicted_category": "other",
                "sentiment": "neutral",
                "priority": "medium",
                "confidence": 0.0,
                "suggested_reply": "Thank you for contacting support. Our team will assist you shortly.",
                "automation_action": "Escalate to human"
            })

        if (i + 1) % 10 == 0:
            pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)
            print(f"Checkpoint saved at {i+1} queries")

        time.sleep(0.5)

    results_df = pd.DataFrame(results)

    results_df.to_csv(OUTPUT_FILE, index=False)

    print("\nBatch processing complete!")
    print(f"Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    run_batch()