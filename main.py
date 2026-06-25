import json
import os
from datetime import datetime

# PROJECT: Mini CRM
# VERSION: V1 to V5 (Combined Architecture)
# ARCHITECT: Prince Victor

DB_FILE = 'customers.json'

# --- V1/V2/V3: CORE MEMORY & COMMANDS ---
# V1: Basic list.
# V2: Initial status logic.
# V3: Advanced commands (Upgrade, Find, Count).

# --- V4: PERSISTENCE LAYER ---
def load_customers():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_customers(customers):
    try:
        with open(DB_FILE, 'w') as f:
            json.dump(customers, f, indent=4)
    except IOError as e:
        print(f'Error saving: {e}')

# --- V5: REVOPS ENGINE (RBAC, SOFT DELETE, AUDIT) ---
def normalize_input(data):
    return data.strip().lower()

def validate_customer(customers, email, phone):
    for customer in customers:
        if customer.get("email") == email or customer.get("phone") == phone:
            return False
    return True

def add_customer(customers, name, status, email, phone, role):
    if role != "Admin": return "Access Denied."
    if not all([name, status, email, phone]): return "All fields required."
    if not validate_customer(customers, email, phone): return "Duplicate email/phone."
    
    now = datetime.now().isoformat()
    new_customer = {
        "name": name, "status": status, "email": email, "phone": phone,
        "is_deleted": False, "created_at": now, "updated_at": now
    }
    customers.append(new_customer)
    save_customers(customers)
    return "Added."

def search_customers(customers, query=None):
    active = [c for c in customers if not c.get("is_deleted")]
    if not query: return active
    q = normalize_input(query)
    return [c for c in active if q in c["name"].lower() or q in c["email"].lower()]

def upgrade_customer(customers, email, role):
    if role != "Admin": return "Access Denied."
    for c in customers:
        if c["email"] == email and not c.get("is_deleted"):
            c["status"] = "VIP"
            c["updated_at"] = datetime.now().isoformat()
            save_customers(customers)
            return "Upgraded."
    return "Not found."

def soft_delete_customer(customers, email, role):
    if role != "Admin": return "Access Denied."
    for c in customers:
        if c["email"] == email:
            c["is_deleted"] = True
            c["updated_at"] = datetime.now().isoformat()
            save_customers(customers)
            return "Archived."
    return "Not found."

def get_report(customers):
    active = [c for c in customers if not c.get("is_deleted")]
    vips = [c for c in active if c["status"] == "VIP"]
    return {"Active": len(active), "VIPs": len(vips)}

def main_menu():
    print("
--- CRM MASTER ENGINE (V1-V5) ---")
    customers = load_customers()
    role = input("Role (Admin/Reader): ").strip().capitalize()
    while True:
        print("
1. Add  2. Search  3. Upgrade  4. Delete  5. Report  6. Exit")
        choice = input("Action: ")
        if choice == "1":
            print(add_customer(customers, input("Name: "), input("Status: "), input("Email: "), input("Phone: "), role))
        elif choice == "2":
            for r in search_customers(customers, input("Search: ")): print(f"[{r['status']}] {r['name']} ({r['email']})")
        elif choice == "3": print(upgrade_customer(customers, input("Email: "), role))
        elif choice == "4": print(soft_delete_customer(customers, input("Email: "), role))
        elif choice == "5": print(get_report(customers))
        elif choice == "6": break

if __name__ == "__main__":
    main_menu()
