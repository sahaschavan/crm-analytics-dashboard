import pandas as pd
from datetime import datetime
from database import fetch_all_clients
 
def days_since_contact(date_str):
    last = datetime.strptime(date_str, '%Y-%m-%d')
    return (datetime.now() - last).days
 
def compute_engagement_score(row):
    meeting_score = min(row['meetings_ytd'] / 20 * 40, 40)
    email_score   = min(row['emails_ytd'] / 50 * 30, 30)
    days_ago      = days_since_contact(row['last_contact'])
    recency_score = max(0, 30 - (days_ago / 180 * 30))
    return round(meeting_score + email_score + recency_score, 1)
 
def assign_priority(row):
    high_stages = ['Negotiation', 'Proposal']
    if row['aum_millions'] > 1000 or row['deal_stage'] in high_stages:
        return 'HIGH'
    elif row['aum_millions'] > 300:
        return 'MEDIUM'
    return 'LOW'
 
def assign_risk_flag(row):
    days_ago = days_since_contact(row['last_contact'])
    if days_ago > 90 and row['engagement_score'] < 30:
        return 'AT RISK'
    elif days_ago > 60:
        return 'MONITOR'
    return 'HEALTHY'
 
def run_analytics():
    df = fetch_all_clients()
    df['engagement_score'] = df.apply(compute_engagement_score, axis=1)
    df['priority']         = df.apply(assign_priority, axis=1)
    df['risk_flag']        = df.apply(assign_risk_flag, axis=1)
    df['days_since_contact'] = df['last_contact'].apply(days_since_contact)
    return df
 
if __name__ == '__main__':
    df = run_analytics()
    print('\n--- Analytics Summary ---')
    print(f'Total Clients: {len(df)}')
    print(f'At Risk: {(df.risk_flag == "AT RISK").sum()}')
    print(f'High Priority: {(df.priority == "HIGH").sum()}')
    print(f'Avg Engagement Score: {df.engagement_score.mean():.1f}')
