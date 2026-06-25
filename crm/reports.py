from .database import get_connection
def get_dashboard():
    conn = get_connection(); cursor = conn.cursor()
    cursor.execute('SELECT status, COUNT(*) FROM Leads WHERE is_deleted = 0 GROUP BY status')
    pipeline = cursor.fetchall()
    cursor.execute('SELECT COUNT(*) FROM Leads WHERE is_deleted = 1')
    deleted = cursor.fetchone()[0]
    conn.close(); return {'pipeline': pipeline, 'deleted_count': deleted}
