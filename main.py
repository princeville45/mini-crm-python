import json
import os
from datetime import datetime

# CRM V5 BUILD SPECIFICATION - PRINCE VICTOR
# PROJECT NAME: Mini CRM V5 (The RevOps Engine)
# OBJECTIVE: Professional Modularization, Soft Delete, RBAC, and Audit Timestamps.
# CONTINUATION: Upgraded from V4 Persistent JSON Core.

DB_FILE = "customers.json"

# --- LAYER 1: DATA PERISTENCE & NORMALIZATION ---

def load_customers():
    """V4 Legacy: Self-Healing Loader"""
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_customers(customers):
    """V4 Legacy: Persistent Saver"""
    try:
        with open(DB_FILE, "w") as f:
            json.dump(customers, f, indent=4)
    except IOError as e:
        print(f"Error saving database: {e}")

def normalize_input(data):
    """New V5: Prevent Duplicate fragmentation"""
    return data.strip().lower()

# --- LAYER 2: VALIDATION & INTEGRITY ---

def validate_customer(customers, email, phone):
    """New V5: Unique Constraint Enforcement (SQL Logic)"""
    for customer in customers:
        if customer.get("email") == email or customer.get("phone") == phone:
            return False
    return True

# --- LAYER 3: CRUD OPERATIONS (THE ENGINE) ---

def add_customer(customers, name, status, email, phone, role):
    """Upgraded V5: RBAC + Integrity + Timestamps"""
    if role != "Admin":
        return "Access Denied: Admin permissions required."
    
    if not all([name, status, email, phone]):
        return "Error: All fields (Name, Status, Email, Phone) are required."

    if not validate_customer(customers, email, phone):
        return "Error: Customer with this email or phone already exists."

    now = datetime.now().isoformat()
    new_customer = {
        "name": name,
        "status": status,
        "email": email,
        "phone": phone,
        "is_deleted": False,
        "created_at": now,
        "updated_at": now
    }
    
    customers.append(new_customer)
    save_customers(customers)
    return f"Customer {name} added successfully."

def search_customers(customers, query=None):
    """New V5: Filtered Search (Excludes Soft Deleted)"""
    active_leads = [c for c in customers if not c.get("is_deleted", False)]
    if not query:
        return active_leads
    
    query = normalize_input(query)
    return [c for c in active_leads if query in c["name"].lower() or query in c["email"].lower()]

def upgrade_customer(customers, email, role):
    """Upgraded V5: RBAC + Timestamp Update"""
    if role != "Admin":
        return "Access Denied."
    
    for customer in customers:
        if customer["email"] == email and not customer.get("is_deleted"):
            customer["status"] = "VIP"
            customer["updated_at"] = datetime.now().isoformat()
            save_customers(customers)
            return "Upgrade Successful."
    return "Customer not found."

def soft_delete_customer(customers, email, role):
    """New V5: Soft Delete Protocol"""
    if role != "Admin":
        return "Access Denied."
    
    for customer in customers:
        if customer["email"] == email:
            customer["is_deleted"] = True
            customer["updated_at"] = datetime.now().isoformat()
            save_customers(customers)
            return "Customer soft-deleted (archived)."
    return "Customer not found."

# --- LAYER 4: REPORTING & INSIGHTS ---

def get_revenue_report(customers):
    """New V5: Aggregate Insights"""
    active = [c for c in customers if not c.get("is_deleted")]
    vips = [c for c in active if c["status"] == "VIP"]
    
    return {
        "Total Active Leads": len(active),
        "VIP Count": len(vips),
        "Conversion Rate": f"{(len(vips)/len(active)*100 if active else 0):.2f}%"
    }

# --- LAYER 5: INTERFACE & SESSION ---

def main_menu():
    print("\n--- CRM V5 REVOPS ENGINE ---")
    customers = load_customers()
    
    # Simple RBAC Session Start
    user_input = input("Enter Role (Admin/Reader): ").strip().capitalize()
    role = user_input if user_input in ["Admin", "Reader"] else "Reader"
    print(f"Session Started as: {role}")

    while True:
        print("\n1. Add Lead (Admin Only)")
        print("2. Search/List Leads")
        print("3. Upgrade to VIP (Admin Only)")
        print("4. Soft Delete Lead (Admin Only)")
        print("5. Revenue Report")
        print("6. Exit")
        
        choice = input("Select Option: ")
        
        if choice == "1":
            name = input("Name: ")
            status = input("Status: ")
            email = input("Email: ")
            phone = input("Phone: ")
            print(add_customer(customers, name, status, email, phone, role))
            
        elif choice == "2":
            query = input("Search (Enter for all): ")
            results = search_customers(customers, query)
            for r in results:
                print(f"[{r['status']}] {r['name']} - {r['email']} (Added: {r['created_at'][:10]})")
                
        elif choice == "3":
            email = input("Email of lead to upgrade: ")
            print(upgrade_customer(customers, email, role))
            
        elif choice == "4":
            email = input("Email of lead to archive: ")
            print(soft_delete_customer(customers, email, role))
            
        elif choice == "5":
            report = get_revenue_report(customers)
            for key, val in report.items():
                print(f"{key}: {val}")
                
        elif choice == "6":
            print("System Shutdown.")
            break

if __name__ == "__main__":
    main_menu()
