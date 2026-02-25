import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
import random
from faker import Faker
from datetime import datetime, timedelta

fake=Faker()
random.seed(42)

DEAL_STAGES=['Prospect', 'Qualified', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
REGIONS=['Americas', 'EMEA', 'Asia Pacific']
PRODUCTS=['Equities', 'Fixed Income', 'FX', 'Derivatives', 'Research']

def generate_clients(n=50):
    clients=[]
    for i in range (n):
        last_contact=datetime.now()-timedelta(days=random.randint(1,180))
        clients.append({'client_id':     f'CLT{1000 + i}',
                        'client_name':   fake.company(),
                        'contact_name':  fake.name(),
                        'region':        random.choice(REGIONS),
                        'product':       random.choice(PRODUCTS),
                        'aum_millions':  round(random.uniform(10, 5000), 2),
                        'deal_stage':    random.choice(DEAL_STAGES),
                        'meetings_ytd':  random.randint(0, 20),
                        'emails_ytd':    random.randint(0, 50),
                        'last_contact':  last_contact.strftime('%Y-%m-%d'),
                        'revenue_ytd':   round(random.uniform(5000, 500000), 2),})
    return pd.DataFrame(clients)

if __name__=='__main__':
    df=generate_clients()
    df.to_csv('clients.csv', index=False)
    df.insert(0, 'sr_no', range(1, len(df) + 1))
    print (df.to_string(index=False))