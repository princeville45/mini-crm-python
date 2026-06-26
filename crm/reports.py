import sqlite3
import logging
from .database import get_connection

logger = logging.getLogger(__name__)

def get_dashboard():
    conn = get_connection()
    if not conn: return {'pipeline': [], 'deleted_count': 0, 'hot_leads': []}
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT status, COUNT(*) FROM Leads WHERE is_deleted = 0 GROUP BY status')
        pipeline = cursor.fetchall()
        
        cursor.execute('SELECT COUNT(*) FROM Leads WHERE is_deleted = 1')
        deleted = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT L.name, COUNT(I.id) as score 
            FROM Leads L 
            LEFT JOIN Interactions I ON L.id = I.lead_id 
            WHERE L.is_deleted = 0 
            GROUP BY L.id 
            ORDER BY score DESC 
            LIMIT 5
        ''')
        hot_leads = cursor.fetchall()
        return {'pipeline': pipeline, 'deleted_count': deleted, 'hot_leads': hot_leads}
    except sqlite3.Error as e:
        logger.error(f"Error generating dashboard: {e}")
        return {'pipeline': [], 'deleted_count': 0, 'hot_leads': []}
    finally:
        conn.close()
