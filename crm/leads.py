from .database import get_connection
VALID_STATUSES = ['New', 'Contacted', 'Interested', 'Proposal Sent', 'Won', 'Lost']
def add_lead(name, status, email, phone):
    if status not in VALID_STATUSES: status = 'New'
    conn = get_connection(); cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO Leads (name, status, email, phone) VALUES (?, ?, ?, ?)', (name, status, email, phone))
        conn.commit(); return 'Lead Added.'
    except Exception as e: return str(e)
    finally: conn.close()
def update_lead(email, **kwargs):
    conn = get_connection(); cursor = conn.cursor()
    fields = ', '.join([f'{k} = ?' for k in kwargs.keys()])
    values = list(kwargs.values()) + [email]
    cursor.execute(f'UPDATE Leads SET {fields}, updated_at = CURRENT_TIMESTAMP WHERE email = ?', values)
    conn.commit(); conn.close(); return 'Updated.'
def soft_delete(email): return update_lead(email, is_deleted=1)
def restore_lead(email): return update_lead(email, is_deleted=0)
def get_leads(query=None, status=None):
    conn = get_connection(); cursor = conn.cursor()
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
    res = cursor.fetchall(); conn.close(); return res
