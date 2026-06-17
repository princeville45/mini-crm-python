# Step 1: Create the leads
leads = [
    {"name": "Victor", "score": 90},
    {"name": "Ruby", "score": 65},
    {"name": "James", "score": 40}
]

# Step 2: Create the classifier
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

print(f"\n--- Searching for: {search_name} ---")
for lead in leads:
    if lead["name"] == search_name:
        status = classify_lead(lead)
        print(f"Found: {lead['name']} | Status: {status} | Score: {lead['score']}")
        found = True
        break

if not found:
    print(f"Result: Customer '{search_name}' not found in the database.")

print(f"\nFinal Lead Count: {len(leads)}")
