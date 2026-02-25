import sqlite3
import pandas as pd
from data_generator import generate_clients
 
DB_PATH = 'crm.db'
 
def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            client_id     TEXT PRIMARY KEY,
            client_name   TEXT NOT NULL,
            contact_name  TEXT,
            region        TEXT,
            product       TEXT,
            aum_millions  REAL,
            deal_stage    TEXT,
            meetings_ytd  INTEGER,
            emails_ytd    INTEGER,
            last_contact  TEXT,
            revenue_ytd   REAL
        )
    ''')
    conn.commit()
    conn.close()
    print('Database and table created.')
 
def load_data():
    df = generate_clients()
    conn = sqlite3.connect(DB_PATH)
    df.to_sql('clients', conn, if_exists='replace', index=False)
    conn.close()
    print(f'Loaded {len(df)} clients into database.')
 
def fetch_all_clients():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql('SELECT * FROM clients', conn)
    conn.close()
    return df
 
if __name__ == '__main__':
    create_database()
    load_data()
    df = fetch_all_clients()
    print(df)
