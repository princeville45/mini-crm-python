import json
import os
import sqlite3
from datetime import datetime

# PROJECT: Mini CRM V5 - FINAL REVOPS EDITION
# ARCHITECT: Prince Victor
# CONTINUATION: Consolidated V1-V5 with SQL/Relational Intelligence.

DB_JSON = 'customers.json'
DB_SQL = 'crm_engine.db'

# --- LAYER 1: HYBRID PERSISTENCE & SQL INITIALIZATION ---

def init_sqlite():
    conn = sqlite3.connect(DB_SQL)
    cursor = conn.cursor()
    # Table 1: Leads
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        status TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT UNIQUE NOT NULL,
        is_deleted BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    # Table 2: Interactions (Relational Logic)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lead_id INTEGER,
        note TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (lead_id) REFERENCES Leads (id)
    )""")
    conn.commit()
    return conn

def migrate_json_to_sql():
    """Hybrid Persistence: Bridges Legacy JSON to the SQL Vault"""
    if not os.path.exists(DB_JSON): return
    
    conn = init_sqlite()
    cursor = conn.cursor()
    
    with open(DB_JSON, 'r') as f:
        customers = json.load(f)
        
    for c in customers:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO Leads (name, status, email, phone, is_deleted, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (c['name'], c['status'], c['email'], c['phone'], c.get('is_deleted', 0), c.get('created_at'), c.get('updated_at')))
        except: continue
        
    conn.commit()
    conn.close()
    print("[SYSTEM] Hybrid Migration Complete. Data is now in the SQL Vault.")

# --- LAYER 2: VALIDATION & RBAC ---

def is_admin(role):
    return role == "Admin"

# --- LAYER 3: CRUD OPERATIONS (SQL POWERED) ---

def add_lead(name, status, email, phone, role):
    if not is_admin(role): return "Access Denied."
    conn = init_sqlite()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Leads (name, status, email, phone) VALUES (?, ?, ?, ?)", 
                       (name, status, email, phone))
        conn.commit()
        return "Lead Added Successfully."
    except sqlite3.IntegrityError:
        return "Error: Email or Phone already exists (UNIQUE Constraint)."
    finally:
        conn.close()

def log_interaction(email, note):
    """Relational Logic: Connects an interaction to a specific Lead ID"""
    conn = init_sqlite()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Leads WHERE email = ?", (email,))
    lead = cursor.fetchone()
    if lead:
        cursor.execute("INSERT INTO Interactions (lead_id, note) VALUES (?, ?)", (lead[0], note))
        conn.commit()
        conn.close()
        return "Interaction Logged."
    conn.close()
    return "Lead not found."

def search_leads(query, role):
    conn = init_sqlite()
    cursor = conn.cursor()
    sql = "SELECT name, status, email FROM Leads WHERE is_deleted = 0"
    if query:
        sql += " AND (name LIKE ? OR email LIKE ?)"
        cursor.execute(sql, (f'%{query}%', f'%{query}%'))
    else:
        cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return results

def soft_delete_lead(email, role):
    if not is_admin(role): return "Access Denied."
    conn = init_sqlite()
    cursor = conn.cursor()
    cursor.execute("UPDATE Leads SET is_deleted = 1, updated_at = CURRENT_TIMESTAMP WHERE email = ?", (email,))
    conn.commit()
    conn.close()
    return "Lead Archived (Soft Deleted)."

# --- LAYER 4: REPORTING ---

def get_velocity_report():
    """Lead Velocity Module: Aggregate Intelligence"""
    conn = init_sqlite()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Leads WHERE is_deleted = 0")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Leads WHERE status = 'VIP' AND is_deleted = 0")
    vips = cursor.fetchone()[0]
    conn.close()
    return {"Total Leads": total, "VIPs": vips}

# --- INTERFACE ---

def main_menu():
    print("
--- CRM V5 FINAL MASTER ENGINE ---")
    migrate_json_to_sql() # Legacy Bridge
    role = input("Role (Admin/Reader): ").strip().capitalize()
    
    while True:
        print("
1. Add Lead  2. Search  3. Log Interaction  4. Delete  5. Velocity Report  6. Exit")
        choice = input("Select: ")
        if choice == "1":
            print(add_lead(input("Name: "), input("Status: "), input("Email: "), input("Phone: "), role))
        elif choice == "2":
            res = search_leads(input("Query: "), role)
            for r in res: print(f"[{r[1]}] {r[0]} ({r[2]})")
        elif choice == "3":
            print(log_interaction(input("Email: "), input("Note: ")))
        elif choice == "4":
            print(soft_delete_lead(input("Email: "), role))
        elif choice == "5":
            print(get_velocity_report())
        elif choice == "6": break

if __name__ == "__main__":
    main_menu()
