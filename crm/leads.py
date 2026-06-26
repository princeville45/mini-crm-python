import sqlite3
import logging
from .database import get_connection

logger = logging.getLogger(__name__)
VALID_STATUSES = ['New', 'Contacted', 'Interested', 'Proposal Sent', 'Won', 'Lost']

def add_lead(name, status, email, phone):
    if status not in VALID_STATUSES: status = 'New'
    conn = get_connection()
    if not conn: return "Connection Failed."
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Leads (name, status, email, phone) VALUES (?, ?, ?, ?)', (name, status, email, phone))
        conn.commit()
        logger.info(f"Lead added: {email}")
        return 'Lead Added.'
    except sqlite3.IntegrityError:
        return 'Error: Email or Phone already exists.'
    except sqlite3.Error as e:
        logger.error(f"Error adding lead: {e}")
        return f"Database Error: {e}"
    finally:
        conn.close()

def update_lead(email, **kwargs):
    conn = get_connection()
    if not conn: return "Connection Failed."
    try:
        cursor = conn.cursor()
        fields = ', '.join([f'{k} = ?' for k in kwargs.keys()])
        values = list(kwargs.values()) + [email]
        cursor.execute(f'UPDATE Leads SET {fields}, updated_at = CURRENT_TIMESTAMP WHERE email = ?', values)
        conn.commit()
        logger.info(f"Lead updated: {email}")
        return 'Updated.'
    except sqlite3.Error as e:
        logger.error(f"Error updating lead {email}: {e}")
        return f"Database Error: {e}"
    finally:
        conn.close()

def soft_delete(email): return update_lead(email, is_deleted=1)
def restore_lead(email): return update_lead(email, is_deleted=0)

def get_leads(query=None, status=None):
    conn = get_connection()
    if not conn: return []
    try:
        cursor = conn.cursor()
        sql = 'SELECT * FROM Leads WHERE is_deleted = 0'
        params = []
        if query:
            sql += ' AND (name LIKE ? OR email LIKE ? OR phone LIKE ?)'
            params.extend([f"%{query}%", f"%{query}%", f"%{query}%"])
        if status in VALID_STATUSES:
            sql += ' AND status = ?'
            params.append(status)
        sql += ' ORDER BY created_at DESC'
        cursor.execute(sql, params)
        return cursor.fetchall()
    except sqlite3.Error as e:
        logger.error(f"Error fetching leads: {e}")
        return []
    finally:
        conn.close()
