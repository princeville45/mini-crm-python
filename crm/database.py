import sqlite3
DB_SQL = 'crm_engine.db'
def get_connection(): return sqlite3.connect(DB_SQL)
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS Leads (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, status TEXT NOT NULL, email TEXT UNIQUE NOT NULL, phone TEXT UNIQUE NOT NULL, is_deleted BOOLEAN DEFAULT 0, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    cursor.execute('CREATE TABLE IF NOT EXISTS Interactions (id INTEGER PRIMARY KEY AUTOINCREMENT, lead_id INTEGER, note TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (lead_id) REFERENCES Leads (id))')
    conn.commit()
    conn.close()
