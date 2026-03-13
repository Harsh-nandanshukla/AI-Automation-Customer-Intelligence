# AI Customer Support Automation Plan — Beastlife

## Objective
Use AI to automatically understand, classify, and resolve customer
queries across WhatsApp, Instagram DMs, and Email — reducing manual
support workload and improving response time from hours to seconds.

---

## System Workflow

Customer Message Received
        ↓
AI Classifier (GPT-4o-mini + LangChain + Few-Shot Prompting)
        ↓
Category + Sentiment + Confidence Score + Suggested Reply
        ↓
Confidence Threshold Check (< 0.75 → Escalate immediately)
        ↓
Priority Assignment (angry → high, frustrated → medium, others → low)
        ↓
Automation Decision Engine
        ↓
Auto-Resolved  ←————→  Escalated to Human

---

## Enhancements Implemented

### 1. Suggested Reply Generation
The classifier now generates a short automated reply alongside
category and sentiment in the same API call. This enables the
system to suggest an immediate response for every query without
any additional cost or latency.

Example output for an order status query:
> "We're sorry for the wait! Your order is being processed and
> we'll share your tracking link shortly."

### 2. Confidence-Based Escalation Gate
A confidence threshold of 0.75 was introduced. Any query where
the model confidence falls below this threshold is automatically
routed to a human agent regardless of category. This prevents
incorrect automated responses from reaching frustrated customers.

| Confidence | Action |
|---|---|
| ≥ 0.75 | Proceed with automation decision |
| < 0.75 | Escalate to human immediately |

### 3. Priority Assignment
Each classified query receives a priority level based on sentiment:

| Sentiment | Priority | Target Response Time |
|---|---|---|
| angry | high | 5 minutes |
| frustrated | medium | 15 minutes |
| neutral | low | 1 hour |
| positive | low | 4 hours |

Angry sentiment overrides all automation rules — even
auto-resolvable categories are escalated when a customer
is detected as angry.

### 4. Few-Shot Prompting for Edge Cases
Few-shot examples were added directly to the classification
prompt for the most common boundary cases identified during
testing:

- order_status vs delivery_delay
- payment_failure vs refund_request

This improved handling of semantically overlapping queries
and reduced label ambiguity errors.

### 5. Dashboard CSV Export
A download button was added to the Streamlit dashboard so
support managers can export classified results for offline
analysis, reporting, or integration with external tools.

---

## Automation Decision Logic

| Category | Confidence | Sentiment | Action |
|---|---|---|---|
| order_status | ≥ 0.75 | any | Auto-reply with tracking link |
| delivery_delay | ≥ 0.75 | neutral | Auto-reply with ETA update |
| delivery_delay | ≥ 0.75 | angry/frustrated | Escalate to human |
| refund_request | any | any | Always escalate (financial) |
| product_issue | any | any | Always escalate + flag QA |
| subscription_issue | ≥ 0.75 | any | Auto-reply with self-service |
| payment_failure | ≥ 0.85 | any | Auto-reply with retry link |
| general_query | ≥ 0.75 | any | Auto-reply from FAQ |
| any category | < 0.75 | any | Escalate — low confidence |
| any category | any | angry | Override — always escalate |

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
- Financial decisions always require human approval

### 4. Product Issues (Auto-Resolve Rate: ~0% — Always Escalated)
- Auto-acknowledge with empathy message
- Create QA-flagged support ticket automatically
- Escalate to human agent with full query context attached
- Flag product batch for internal quality review if multiple complaints

### 5. Subscription Issues (Auto-Resolve Rate: ~78%)
- Send self-service portal link for pause, cancel, or modify
- Handle flavor or quantity changes via automated subscription API
- Escalate only if customer has been incorrectly charged

### 6. Payment Failures (Auto-Resolve Rate: ~55%)
- Detect duplicate charge vs failed payment from query context
- Send payment retry link automatically
- For duplicate charges, create refund ticket and escalate
- Trigger real-time alert to payment gateway for investigation

### 7. General Queries (Auto-Resolve Rate: ~88%)
- Search FAQ knowledge base using semantic similarity
- Return most relevant answer automatically
- If similarity score below threshold, escalate to human
- Continuously improve FAQ database from resolved queries

---

## Sentiment-Based Priority Queue

When queries reach human agents they are prioritized by sentiment:

Priority 1 — Angry (immediate response target: 5 min)
Priority 2 — Frustrated (target: 15 min)
Priority 3 — Neutral (target: 1 hour)
Priority 4 — Positive (target: 4 hours)

---

## Tools & Architecture

| Layer | Tool | Purpose |
|---|---|---|
| AI Classification | GPT-4o-mini + LangChain | Category + sentiment + reply |
| Few-Shot Prompting | LangChain prompt templates | Edge case accuracy |
| API Backend | FastAPI | Webhook receiver |
| Automation Flows | n8n (self-hosted) | WhatsApp/email auto-replies |
| Dashboard | Streamlit + Plotly | Insights visualization |
| Data Storage | Supabase (PostgreSQL) | Ticket storage and analytics |

---

## How the System Scales

| Volume | Approach |
|---|---|
| 500 queries/day | Single FastAPI server, synchronous calls |
| 5,000 queries/day | Redis queue + Celery workers + vector cache |
| 50,000 queries/day | Horizontal scaling + Pinecone + fine-tuned model |

---

## Expected Business Impact

| Metric | Before AI | After AI |
|---|---|---|
| Avg first response time | 4-6 hours | < 30 seconds |
| Queries requiring human agent | 100% | ~30% |
| Support team capacity needed | 10 agents | 3 agents |
| Customer satisfaction (CSAT) | Baseline | +35% estimated |
| Cost per query resolved | High | Reduced ~70% |

Estimated 70% of queries auto-resolved based on category
distribution from the 50-query dataset analysis.