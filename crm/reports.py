from .database import get_connection
def get_dashboard():
    conn = get_connection(); cursor = conn.cursor()
    cursor.execute('SELECT status, COUNT(*) FROM Leads WHERE is_deleted = 0 GROUP BY status')
    pipeline = cursor.fetchall()
    cursor.execute('SELECT COUNT(*) FROM Leads WHERE is_deleted = 1')
    deleted = cursor.fetchone()[0]
    cursor.execute('SELECT L.name, COUNT(I.id) as score FROM Leads L LEFT JOIN Interactions I ON L.id = I.lead_id WHERE L.is_deleted = 0 GROUP BY L.id ORDER BY score DESC LIMIT 5')
    hot_leads = cursor.fetchall()
    conn.close(); return {'pipeline': pipeline, 'deleted_count': deleted, 'hot_leads': hot_leads}
