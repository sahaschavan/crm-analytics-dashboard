# CRM Analytics Dashboard 
## Features
- Engagement scoring based on meetings, emails, and recency of contact
- Priority flagging (HIGH / MEDIUM / LOW) based on AUM and deal stage
- At-Risk detection for clients with low engagement over 90+ days
- Interactive filters by region, product, and priority
- Pipeline funnel visualization by deal stage
 
## Tech Stack
- Python 3.11 | pandas | SQLite | Streamlit | Plotly | Faker
 
## How to Run
```
pip install -r requirements.txt
python database.py
streamlit run dashboard.py
```
## Business Context
Built to mirror the Client Lifecycle Management and CRM analytics workflows

### Engagement Score (`compute_engagement_score`)
Each client is given a score from 0 to 100 based on three factors:
- **Meetings (40 points max)** — meetings are the most valuable client interaction
- **Emails (30 points max)** — frequency of email communication
- **Recency (30 points max)** — penalizes clients who haven't been contacted recently

### Priority Flag (`assign_priority`)
Each client is flagged HIGH, MEDIUM, or LOW based on business value:
- **HIGH** — AUM over $1 billion, or currently in Proposal/Negotiation stage
- **MEDIUM** — AUM between $300M and $1B
- **LOW** — AUM under $300M and not in an active deal stage

### Risk Flag (`assign_risk_flag`)
Each client is flagged to identify churn risk:
- **AT RISK** — not contacted in 90+ days AND engagement score below 30
- **MONITOR** — not contacted in 60+ days (early warning)
- **HEALTHY** — recently active with good engagement
