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

# TEST DATA
print(add_customer(customers, "Victor", "Regular"))
print(add_customer(customers, "Ruby", "VIP"))
print(add_customer(customers, "James", "Regular"))

print(find_customer(customers, "Victor"))

print(upgrade_customer(customers, "Victor"))
print(upgrade_customer(customers, "Victor"))

print("Total VIP Customers:", count_vips(customers))

print(remove_customer(customers, "Ruby"))

print(customers)
