# Step 1: Create the leads (V1 Legacy)
leads = [
    {"name": "Victor", "score": 90},
    {"name": "Ruby", "score": 65},
    {"name": "James", "score": 40}
]

# Step 2: Create the classifier (V1 Legacy)
def classify_lead(lead):
    if lead["score"] >= 80:
        return "VIP"
    elif lead["score"] >= 50:
        return "Qualified"
    else:
        return "Nurture"

# Step 3: Process all leads
print("--- Initial Batch ---")
for lead in leads:
    status = classify_lead(lead)
    print(f"{lead['name']} -> {status}")

# Step 4: Add a new lead
new_lead = {"name": "Sarah", "score": 80}
leads.append(new_lead)

# Step 5: Run again
print("\n--- Updated Batch (with Sarah) ---")
for lead in leads:
    status = classify_lead(lead)
    print(f"{lead['name']} -> {status}")

# Step 6: Search Engine (Upgrade v2)
search_name = "Sarah"
found = False

print(f"\n--- Searching for: {search_name} (Upgrade V2) ---")
for lead in leads:
    if lead["name"] == search_name:
        status = classify_lead(lead)
        print(f"Found: {lead['name']} | Status: {status} | Score: {lead['score']}")
        found = True
        break

if not found:
    print(f"Result: Customer '{search_name}' not found in the database.")

print(f"\nFinal Lead Count: {len(leads)}")

# --- UPGRADE V3: FUNCTIONAL ENGINE ---
print("\n" + "="*30)
print("UPGRADE V3: FUNCTIONAL ENGINE")
print("="*30)

customers = []

def add_customer(customers, name, status):
    for customer in customers:
        if customer["name"] == name:
            return f"Customer already exists: {name}"
    
    new_customer = {
        "name": name,
        "status": status
    }
    
    customers.append(new_customer)
    return {
        "message": "Customer Added Successfully",
        "customer": new_customer
    }

def find_customer(customers, name):
    for customer in customers:
        if customer["name"] == name:
            return {
                "message": f"Customer Found: {name}",
                "customer": customer
            }
    return f"Customer Not Found: {name}"

def print_customers(customers):
    print("\n--- Current Customer Database ---")
    if not customers:
        print("Database is empty.")
    else:
        for customer in customers:
            print(f"Name: {customer['name']} | Status: {customer['status']}")

def upgrade_customer(customers, name):
    for customer in customers:
        if customer["name"] == name:
            if customer["status"] == "VIP":
                return f"Customer is already VIP: {name}"
            
            customer["status"] = "VIP"
            return {
                "message": "Customer Upgraded Successfully",
                "customer": customer
            }
    return f"Customer Not Found: {name}"

def remove_customer(customers, name):
    for customer in customers:
        if customer["name"] == name:
            customers.remove(customer)
            return f"Customer Removed Successfully: {name}"
    return f"Customer Not Found: {name}"

def count_vips(customers):
    vip_count = 0
    for customer in customers:
        if customer["status"] == "VIP":
            vip_count += 1
    return vip_count

def count_regular(customers):
    regular_count = 0
    for customer in customers:
        if customer["status"] == "Regular":
            regular_count += 1
    return regular_count

def calculate_status_percentage(customers, status):
    if not customers:
        return 0
    count = 0
    for customer in customers:
        if customer["status"] == status:
            count += 1
    return (count / len(customers)) * 100

# TEST DATA (V3 EXECUTION)
print(add_customer(customers, "Victor", "Regular"))
print(add_customer(customers, "Ruby", "VIP"))
print(add_customer(customers, "James", "Regular"))

print("\n--- Searching for: Victor (Upgrade V3) ---")
print(find_customer(customers, "Victor"))

print("\n--- Upgrading Status ---")
print(upgrade_customer(customers, "Victor"))
print(upgrade_customer(customers, "Victor"))

print("\nTotal VIP Customers:", count_vips(customers))
print("Total Regular Customers:", count_regular(customers))

# Percentage Calculations
vip_percent = calculate_status_percentage(customers, "VIP")
reg_percent = calculate_status_percentage(customers, "Regular")

print(f"\n--- Database Analytics ---")
print(f"VIP Percentage: {vip_percent:.2f}%")
print(f"Regular Percentage: {reg_percent:.2f}%")

# Printing the entire database
print_customers(customers)

print("\n--- Removing Customer ---")
print(remove_customer(customers, "Ruby"))

print("\nFinal V3 Customer Database:")
print_customers(customers)
