# AI Customer Care Automation System

Prototype AI system that automatically analyzes customer queries,
categorizes problems, and visualizes insights through a dashboard.

## Full Project Repository
GitHub: https://github.com/Harsh-nandanshukla/AI-Automation-Customer-Intelligence

Includes: workflow_diagram.png, sample_queries.csv,
results.csv, automation_plan.md, all source files

## Features
- AI query classification using OpenAI GPT-4o-mini
- Sentiment detection (positive, neutral, frustrated, angry)
- Automated support action suggestions per category
- Suggested reply generation for each query
- Confidence-based escalation gate (low confidence → human agent)
- Priority assignment (high / medium / low) based on sentiment
- Few-shot prompting for improved edge case accuracy
- Customer support analytics dashboard
- Dynamic business insight generation
- Live query classification demo
- CSV export of classified results

## System Workflow
Customer Message
→ AI Classification (GPT-4o-mini + LangChain)
→ Sentiment Detection
→ Confidence Threshold Check
→ Priority Assignment
→ Automation Decision Engine
→ Data Storage (results.csv)
→ Analytics Dashboard (Streamlit)

## Project Structure

| File | Purpose |
|---|---|
| `classifier.py` | AI classification, sentiment, priority, suggested reply, escalation logic |
| `run_batch.py` | Batch classification of 50 sample queries |
| `dashboard.py` | Streamlit analytics dashboard with export |
| `sample_queries.csv` | 50 diverse customer queries across 8 categories |
| `results.csv` | Generated classification results |
| `automation_plan.md` | Automation opportunities and escalation logic |
| `workflow_diagram.png` | System architecture diagram |

## Installation

Create virtual environment:
```bash
python -m venv aics
```

Activate (Windows PowerShell):
```bash
.\aics\Scripts\Activate.ps1
```

Install dependencies:
```bash
pip install langchain langchain-openai openai chromadb streamlit pandas plotly numpy python-dotenv
```

Set up environment variables — create a `.env` file in root folder:
```
OPENAI_API_KEY=your-openai-api-key-here
```

## Run the System

Step 1 — Generate classification results:
```bash
python run_batch.py
```

Step 2 — Launch dashboard:
```bash
streamlit run dashboard.py
```

Step 3 — Open browser:
```
http://localhost:8501
```

## Model Performance
- 50 queries classified across 8 categories
- 94%+ classification accuracy
- 2 borderline misclassifications due to label ambiguity
  (order_status vs delivery_delay — reasonable either way)
- Average confidence score: ~0.89
- Few-shot prompting added to reduce edge case errors

## Enhancements Implemented

### 1. Suggested Reply Generation
The classifier generates a short automated support reply along
with category and sentiment, enabling the system to suggest
immediate responses for common queries.

### 2. Confidence-Based Escalation Gate
Queries with model confidence below 0.75 are automatically
escalated to human support, preventing incorrect automated
responses from reaching customers.

### 3. Priority Assignment
Each query is assigned a priority level (high / medium / low)
based on detected sentiment. Angry customers are always flagged
as high priority regardless of category.

### 4. Few-Shot Prompting for Edge Cases
Few-shot examples were added to the classification prompt to
improve accuracy on ambiguous boundary cases such as
delivery_delay vs order_status queries.

### 5. Dashboard CSV Export
A download button was added to the Streamlit dashboard allowing
users to export the full analyzed results as CSV, making the
system practical for ongoing analytics workflows.

## Scaling Strategy

| Volume | Approach |
|---|---|
| 500 queries/day | Single FastAPI server, synchronous calls |
| 5,000 queries/day | Redis queue + Celery workers + vector cache |
| 50,000 queries/day | Horizontal scaling + Pinecone + fine-tuned model |

## Expected Impact
AI automation resolves ~70% of queries automatically, reducing
average response time from 4-6 hours to under 30 seconds.