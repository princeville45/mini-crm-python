import json
import os

# CRM V4 BUILD SPECIFICATION
# PROJECT NAME: Mini CRM V4
# OBJECTIVE: Convert CRM V3 from RAM-only storage to persistent JSON storage.

DB_FILE = "customers.json"

def load_customers():
    """Feature 2: Load Customers / Feature 10: Self Healing"""
    if not os.path.exists(DB_FILE):
        return []
    
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("Warning: Database file corrupted. Starting with empty list.")
        return []

def save_customers(customers):
    """Feature 3: Save Customers"""
    try:
        with open(DB_FILE, "w") as f:
            json.dump(customers, f, indent=4)
    except IOError as e:
        print(f"Error saving database: {e}")

def add_customer(customers, name, status):
    """Feature 4: Add Customer"""
    for customer in customers:
        if customer["name"] == name:
            return "Customer already exists"
    
    customers.append({"name": name, "status": status})
    save_customers(customers)
    return "Customer added successfully"

def remove_customer(customers, name):
    """Feature 5: Remove Customer"""
    for i, customer in enumerate(customers):
        if customer["name"] == name:
            customers.pop(i)
            save_customers(customers)
            return "Customer removed successfully"
    return "Customer not found"

def upgrade_customer(customers, name):
    """Feature 6: Upgrade Customer"""
    for customer in customers:
        if customer["name"] == name:
            if customer["status"] == "VIP":
                return "Customer already VIP"
            customer["status"] = "VIP"
            save_customers(customers)
            return "Customer upgraded successfully"
    return "Customer not found"

def find_customer(customers, name):
    """Feature 7: Find Customer"""
    for customer in customers:
        if customer["name"] == name:
            return customer
    return "Customer not found"

def count_vips(customers):
    """Feature 8: Count VIPs"""
    return sum(1 for c in customers if c.get("status") == "VIP")

# Feature 9: Startup Workflow
if __name__ == "__main__":
    print("--- CRM V4 ENGINE STARTING ---")
    customers = load_customers()
    print(f"Engine Ready. Loaded {len(customers)} customers.")

    # Feature 11: Release Verification
    # Testing the V4 protocol
    print("\n[V4 TEST: ADD]")
    print(add_customer(customers, "Victor", "VIP"))
    print(add_customer(customers, "Ruby", "Qualified"))
    
    print("\n[V4 TEST: FIND]")
    print(f"Searching for Victor: {find_customer(customers, 'Victor')}")
    
    print("\n[V4 TEST: UPGRADE]")
    print(f"Upgrading Ruby: {upgrade_customer(customers, 'Ruby')}")
    
    print("\n[V4 TEST: COUNT]")
    print(f"Total VIPs: {count_vips(customers)}")
    
    print("\n[V4 TEST: PERSISTENCE]")
    print("Check customers.json for persistent data.")
    print("--- CRM V4 OPERATIONAL ---")
