# mini-crm-python
# Customer Relationship Management (CRM)
# Versions: V1, V2, V3

# --- V1: INITIAL CLASSIFIER ---
leads = [
    {"name": "Victor", "score": 90},
    {"name": "Ruby", "score": 65},
    {"name": "James", "score": 40}
]

def classify_lead(lead):
    if lead["score"] >= 80:
        return "VIP"
    elif lead["score"] >= 50:
        return "Qualified"
    else:
        return "Nurture"

print("--- Initial Batch (V1) ---")
for lead in leads:
    status = classify_lead(lead)
    print(f"{lead['name']} -> {status}")

# --- V2: SEARCH ENGINE ---
new_lead = {"name": "Sarah", "score": 80}
leads.append(new_lead)

search_name = "Sarah"
found = False

print(f"\n--- Searching for: {search_name} (V2) ---")
for lead in leads:
    if lead["name"] == search_name:
        status = classify_lead(lead)
        print(f"Found: {lead['name']} | Status: {status} | Score: {lead['score']}")
        found = True
        break

if not found:
    print(f"Result: Customer '{search_name}' not found.")

# --- V3: FUNCTIONAL ENGINE ---
print("\n" + "="*30)
print("V3: FUNCTIONAL ENGINE")
print("="*30)

customers = []

def add_customer(customers, name, status):
    for customer in customers:
        if customer["name"] == name:
            return f"Customer already exists: {name}"
    new_customer = {"name": name, "status": status}
    customers.append(new_customer)
    return {"message": "Customer Added", "customer": new_customer}

def find_customer(customers, name):
    for customer in customers:
        if customer["name"] == name:
            return {"message": "Customer Found", "customer": customer}
    return f"Customer Not Found: {name}"

def print_customers(customers):
    print("\n--- Customer Database ---")
    if not customers:
        print("Empty.")
    else:
        for customer in customers:
            print(f"Name: {customer['name']} | Status: {customer['status']}")

def count_vips(customers):
    return sum(1 for c in customers if c["status"] == "VIP")

def count_regular(customers):
    return sum(1 for c in customers if c["status"] == "Regular")

def calculate_status_percentage(customers, status):
    if not customers: return 0
    count = sum(1 for c in customers if c["status"] == status)
    return (count / len(customers)) * 100

# EXECUTION
print(add_customer(customers, "Victor", "Regular"))
print(add_customer(customers, "Ruby", "VIP"))
print(add_customer(customers, "James", "Regular"))

print("\n--- Analytics ---")
print("VIPs:", count_vips(customers))
print("Regulars:", count_regular(customers))
print(f"VIP %: {calculate_status_percentage(customers, 'VIP'):.2f}%")
print(f"Regular %: {calculate_status_percentage(customers, 'Regular'):.2f}%")

print_customers(customers)
