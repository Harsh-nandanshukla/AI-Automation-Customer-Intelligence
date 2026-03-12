# AI Customer Support Automation Plan — Beastlife

## Objective
Use AI to automatically understand, classify, and resolve customer queries
across WhatsApp, Instagram DMs, and Email — reducing manual support workload
and improving response time from hours to seconds.

---

## System Workflow

Customer Message Received
        ↓
AI Classifier (GPT-4o-mini + LangChain)
        ↓
Category + Sentiment + Confidence Score
        ↓
Automation Decision Engine
        ↓
Auto-Resolved  ←——→  Escalated to Human

---

## Automation Decision Logic

| Category           | Confidence  | Sentiment        | Action                          |
|--------------------|-------------|------------------|---------------------------------|
| order_status       | > 0.80      | any              | Auto-reply with tracking link   |
| delivery_delay     | > 0.80      | neutral          | Auto-reply with ETA update      |
| delivery_delay     | > 0.80      | angry/frustrated | Escalate to human agent         |
| refund_request     | any         | any              | Always escalate (financial)     |
| product_issue      | any         | any              | Always escalate + flag QA team  |
| subscription_issue | > 0.80      | any              | Auto-reply with self-service    |
| payment_failure    | > 0.85      | any              | Auto-reply with retry link      |
| general_query      | > 0.75      | any              | Auto-reply from FAQ search      |
| any category       | < 0.75      | any              | Escalate — low confidence       |
| any category       | any         | angry            | Override to escalate            |

**Key Rule:** If sentiment is angry regardless of category or confidence,
the system escalates to a human agent. Frustrated customers should never
receive a bot-only response.

---

## Automation Per Category

### 1. Order Status (Auto-Resolve Rate: ~90%)
- Fetch order ID from message using entity extraction
- Query internal order management system via API
- Return real-time tracking link and current status automatically
- No human involvement required unless order ID cannot be found

### 2. Delivery Delay (Auto-Resolve Rate: ~65%)
- Send proactive apology message with updated ETA from courier API
- If delay exceeds 5 days, automatically escalate to human agent
- Trigger courier partner webhook to investigate stalled shipments

### 3. Refund Requests (Auto-Resolve Rate: ~0% — Always Escalated)
- Immediately acknowledge receipt with automated message
- Send refund policy document automatically
- Create support ticket and assign to human agent
- Send status update to customer at each stage of refund process
- Financial decisions always require human approval

### 4. Product Issues (Auto-Resolve Rate: ~0% — Always Escalated)
- Auto-acknowledge with empathy message
- Create QA-flagged support ticket automatically
- Escalate to human agent with full query context attached
- Flag product batch for internal quality review if multiple complaints

### 5. Subscription Issues (Auto-Resolve Rate: ~78%)
- Send self-service portal link for pause, cancel, or modify
- Handle flavor/quantity changes via automated subscription API
- Escalate only if customer has been incorrectly charged

### 6. Payment Failures (Auto-Resolve Rate: ~55%)
- Detect duplicate charge vs failed payment from query context
- Send payment retry link automatically
- For duplicate charges, create refund ticket and escalate
- Trigger real-time alert to payment gateway for investigation

### 7. General Queries (Auto-Resolve Rate: ~88%)
- Search FAQ vector database using semantic similarity
- Return most relevant answer automatically
- If similarity score below threshold, escalate to human
- Continuously improve FAQ database from resolved queries

---

## Sentiment-Based Priority Queue

When queries reach human agents, they are prioritized by sentiment:

Priority 1 — Angry customers (immediate response target: 5 min)
Priority 2 — Frustrated customers (target: 15 min)
Priority 3 — Neutral customers (target: 1 hour)
Priority 4 — Positive customers (target: 4 hours)

---

## Tools & Architecture

| Layer              | Tool                        | Purpose                        |
|--------------------|-----------------------------|--------------------------------|
| AI Classification  | GPT-4o-mini + LangChain     | Category + sentiment detection |
| Vector FAQ Search  | Chroma DB                   | Semantic FAQ matching          |
| API Backend        | FastAPI                     | Webhook receiver               |
| Automation Flows   | n8n (self-hosted)           | WhatsApp/email auto-replies    |
| Dashboard          | Streamlit + Plotly          | Insights visualization         |
| Data Storage       | Supabase (PostgreSQL)       | Ticket storage and analytics   |

---

## How the System Scales

**At 500 queries/day (current prototype level)**
- Single FastAPI server handles all classification
- Direct synchronous API calls to OpenAI
- Chroma runs locally for FAQ search

**At 5,000 queries/day**
- Add Redis queue (Celery) between ingestion and classifier
- Workers process queries asynchronously in parallel
- Vector cache handles 60-70% of queries without LLM call
- Cost stays low — most common queries never hit the API

**At 50,000 queries/day**
- Horizontal scaling of FastAPI workers
- Pinecone replaces Chroma for distributed vector search
- Fine-tuned classification model replaces GPT-4o-mini
- Real-time Kafka stream for multi-platform ingestion

---

## Expected Business Impact

| Metric                        | Before AI    | After AI       |
|-------------------------------|--------------|----------------|
| Avg first response time       | 4-6 hours    | < 30 seconds   |
| Queries requiring human agent | 100%         | ~30%           |
| Support team capacity needed  | 10 agents    | 3 agents       |
| Customer satisfaction (CSAT)  | Baseline     | +35% estimated |
| Cost per query resolved       | High         | Reduced ~70%   |

Estimated **70% of queries auto-resolved** based on category
distribution from the 50-query dataset analysis.