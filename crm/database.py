import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_SQL = 'crm_engine.db'

def get_connection():
    try:
        return sqlite3.connect(DB_SQL)
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        return None

def init_db():
    conn = get_connection()
    if not conn: return
    try:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL, 
            status TEXT NOT NULL, 
            email TEXT UNIQUE NOT NULL, 
            phone TEXT UNIQUE NOT NULL, 
            is_deleted BOOLEAN DEFAULT 0, 
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            lead_id INTEGER, 
            note TEXT, 
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
            FOREIGN KEY (lead_id) REFERENCES Leads (id)
        )''')
        conn.commit()
        logger.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error initializing database: {e}")
    finally:
        conn.close()
