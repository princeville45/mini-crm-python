import sqlite3
import logging
from .database import get_connection
from .config import VALID_STATUSES, STATUS_NEW

logger = logging.getLogger(__name__)

def add_lead(name, status, email, phone):
    if status not in VALID_STATUSES: status = STATUS_NEW
    conn = get_connection()
    if not conn: return "DB Error."
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Leads (name, status, email, phone) VALUES (?, ?, ?, ?)', 
                       (name, status, email, phone))
        conn.commit()
        return 'Lead Added Successfully.'
    except sqlite3.IntegrityError: return 'Duplicate Email/Phone Error.'
    finally: conn.close()

def update_lead(email, **kwargs):
    conn = get_connection()
    if not conn: return "DB Error."
    fields = ', '.join([f'{k} = ?' for k in kwargs.keys()])
    values = list(kwargs.values()) + [email]
    conn.execute(f'UPDATE Leads SET {fields}, updated_at = CURRENT_TIMESTAMP WHERE email = ?', values)
    conn.commit(); conn.close(); return 'Lead Updated.'

def soft_delete(email): return update_lead(email, is_deleted=1)
def restore_lead(email): return update_lead(email, is_deleted=0)

def search_leads(query=None, status_filter=None):
    conn = get_connection()
    cursor = conn.cursor()
    sql = 'SELECT * FROM Leads WHERE is_deleted = 0'
    params = []
    if query:
        sql += ' AND (name LIKE ? OR email LIKE ? OR phone LIKE ?)'
        params.extend([f"%{query}%", f"%{query}%", f"%{query}%"])
    if status_filter in VALID_STATUSES:
        sql += ' AND status = ?'
        params.append(status_filter)
    cursor.execute(sql + ' ORDER BY created_at DESC', params)
    res = cursor.fetchall(); conn.close(); return res
