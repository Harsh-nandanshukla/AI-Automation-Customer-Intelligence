import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
from classifier import classify_query

RESULTS_FILE = "results.csv"

st.set_page_config(
    page_title="AI Customer Intelligence Dashboard",
    layout="wide"
)

st.title("AI Customer Support Intelligence Dashboard")

# ===============================
# Load Data Safely
# ===============================

def load_data():
    if not os.path.exists(RESULTS_FILE):
        st.warning("results.csv not found. Run run_batch.py first.")
        return pd.DataFrame()

    try:
        df = pd.read_csv(RESULTS_FILE)
        return df
    except Exception as e:
        st.error(f"Failed to load results.csv: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()
# ===============================
# Download Results Button
# ===============================
st.subheader("Export Data")

st.download_button(
    label="Download Results CSV",
    data=df.to_csv(index=False),
    file_name="results.csv",
    mime="text/csv"
)
# ===============================
# Validate Required Columns
# ===============================

required_columns = [
    "query",
    "predicted_category",
    "sentiment",
    "confidence",
    "automation_action"
]

missing = [c for c in required_columns if c not in df.columns]

if missing:
    st.error(f"Missing required columns in dataset: {missing}")
    st.stop()

# ===============================
# Precompute Metrics
# ===============================

category_pct = df["predicted_category"].value_counts(normalize=True) * 100
angry_pct = (df["sentiment"].isin(["angry", "frustrated"])).mean() * 100
auto_resolvable = df[~df["predicted_category"].isin(["product_issue", "other"])].shape[0]
auto_pct = (auto_resolvable / len(df)) * 100

accuracy = None
if "expected_category" in df.columns:
    accuracy = (df["expected_category"] == df["predicted_category"]).mean() * 100

# ===============================
# Overview Metrics
# ===============================

st.subheader("Overview Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Queries", len(df))
col2.metric("Unique Categories", df["predicted_category"].nunique())
col3.metric("Avg Confidence", round(df["confidence"].mean(), 2))

if accuracy is not None:
    col4, col5, col6 = st.columns(3)
    col4.metric("Model Accuracy", f"{accuracy:.1f}%")
    col5.metric("Auto-Resolvable Queries", f"{auto_pct:.1f}%")
    col6.metric("Angry / Frustrated Users", f"{angry_pct:.1f}%")

# ===============================
# Category Distribution
# ===============================

st.subheader("Issue Distribution")

category_counts = df["predicted_category"].value_counts().reset_index()
category_counts.columns = ["Category", "Count"]

colA, colB = st.columns(2)

with colA:
    fig_pie = px.pie(
        category_counts,
        values="Count",
        names="Category",
        title="Query Distribution"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with colB:
    fig_bar = px.bar(
        category_counts,
        x="Category",
        y="Count",
        text="Count",
        title="Query Count by Category"
    )
    fig_bar.update_traces(textposition="outside")
    st.plotly_chart(fig_bar, use_container_width=True)

# ===============================
# Sentiment Distribution
# ===============================

st.subheader("Customer Sentiment")

sentiment_counts = df["sentiment"].value_counts().reset_index()
sentiment_counts.columns = ["Sentiment", "Count"]

fig_sentiment = px.bar(
    sentiment_counts,
    x="Sentiment",
    y="Count",
    title="Sentiment Distribution"
)

st.plotly_chart(fig_sentiment, use_container_width=True)

# ===============================
# Weekly Trend (Simulated)
# ===============================

st.subheader("Query Volume by Category (Simulated Weekly Trend)")

try:
    weeks = ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5"]
    categories = df["predicted_category"].unique()

    np.random.seed(42)  # ensures stable results across refresh

    trend_data = []

    for week in weeks:
        for cat in categories:
            base = df[df["predicted_category"] == cat].shape[0]
            trend_data.append({
                "Week": week,
                "Category": cat,
                "Queries": max(1, int(base * np.random.uniform(0.7, 1.3)))
            })

    trend_df = pd.DataFrame(trend_data)

    fig_trend = px.line(
        trend_df,
        x="Week",
        y="Queries",
        color="Category",
        markers=True,
        title="Weekly Query Volume by Category"
    )

    st.plotly_chart(fig_trend, use_container_width=True)

except Exception as e:
    st.warning(f"Could not generate trend chart: {e}")

# ===============================
# Live Query Classifier
# ===============================

st.subheader("Live Query Classification")

user_query = st.text_area("Enter a customer query")

if st.button("Classify Query"):

    if not user_query.strip():
        st.warning("Please enter a query.")
    else:
        try:
            result = classify_query(user_query)

            st.success("Classification Result")

            c1, c2, c3 = st.columns(3)

            c1.metric("Category", result["category"])
            c2.metric("Sentiment", result["sentiment"])
            c3.metric("Confidence", result["confidence"])

            st.write("Automation Action:")
            st.info(result["automation_action"])

            st.write("Suggested Reply:")
            st.success(result["suggested_reply"])

        except Exception as e:
            st.error(f"Classification failed: {e}")

# ===============================
# Priority Color Styling
# ===============================

def color_priority(val):
    if val == "high":
        return "background-color:#ff4b4b;color:white"
    elif val == "medium":
        return "background-color:#ffa500;color:white"
    elif val == "low":
        return "background-color:#2ecc71;color:white"
    return ""


# ===============================
# Recent Queries Table
# ===============================

st.subheader("Recent Classified Queries")

st.dataframe(
    df[
        [
            "query",
            "predicted_category",
            "sentiment",
            "priority",
            "confidence",
            "automation_action"
        ]
    ].tail(10)
    .style.applymap(color_priority, subset=["priority"]),
    use_container_width=True
)

# ===============================
# Business Insights
# ===============================

st.subheader("Business Insights")

try:

    insights = []

    if category_pct.get("delivery_delay", 0) > 12:
        insights.append("High delivery delay volume** → Integrate real-time courier tracking and proactive delay notifications.")

    if category_pct.get("refund_request", 0) > 10:
        insights.append("Refund requests elevated** → Investigate product quality or shipping issues.")

    if category_pct.get("order_status", 0) > 12:
        insights.append("Order status queries dominate** → Deploy automated tracking chatbot.")

    if category_pct.get("payment_failure", 0) > 8:
        insights.append("Payment failures detected** → Add retry payment flow and better checkout error messages.")

    if category_pct.get("product_issue", 0) > 8:
        insights.append("Product complaints present** → Recommend QA inspection and packaging review.")

    if angry_pct > 30:
        insights.append(f"{angry_pct:.1f}% users are angry/frustrated** → proactive updates could reduce support load.")

    insights.append(f"{auto_pct:.1f}% of queries are auto-resolvable** → chatbot automation could eliminate most manual workload.")

    for insight in insights:
        st.markdown(f"> {insight}")
        st.markdown("")

except Exception as e:
    st.warning(f"Could not compute insights: {e}")