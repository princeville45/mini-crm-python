import json
import os
from datetime import datetime

# CRM V5 BUILD SPECIFICATION - PRINCE VICTOR
# PROJECT NAME: Mini CRM V5 (The RevOps Engine)
# CONTINUATION: Upgraded from V4 Persistent JSON Core.

DB_FILE = 'customers.json'

# --- V4 CORE LOGIC (CONTINUATION) ---

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
        print(f'Error saving database: {e}')

# --- V5 UPGRADES (APPENDED) ---

def normalize_input(data):
    return data.strip().lower()

def validate_customer(customers, email, phone):
    for customer in customers:
        if customer.get('email') == email or customer.get('phone') == phone:
            return False
    return True

def add_customer(customers, name, status, email, phone, role):
    if role != 'Admin':
        return 'Access Denied: Admin permissions required.'
    if not all([name, status, email, phone]):
        return 'Error: All fields are required.'
    if not validate_customer(customers, email, phone):
        return 'Error: Customer with this email or phone already exists.'

    now = datetime.now().isoformat()
    new_customer = {
        'name': name,
        'status': status,
        'email': email,
        'phone': phone,
        'is_deleted': False,
        'created_at': now,
        'updated_at': now
    }
    customers.append(new_customer)
    save_customers(customers)
    return f'Customer {name} added successfully.'

def search_customers(customers, query=None):
    active_leads = [c for c in customers if not c.get('is_deleted', False)]
    if not query:
        return active_leads
    query = normalize_input(query)
    return [c for c in active_leads if query in c['name'].lower() or query in c['email'].lower()]

def upgrade_customer(customers, email, role):
    if role != 'Admin':
        return 'Access Denied.'
    for customer in customers:
        if customer['email'] == email and not customer.get('is_deleted'):
            customer['status'] = 'VIP'
            customer['updated_at'] = datetime.now().isoformat()
            save_customers(customers)
            return 'Upgrade Successful.'
    return 'Customer not found.'

def soft_delete_customer(customers, email, role):
    if role != 'Admin':
        return 'Access Denied.'
    for customer in customers:
        if customer['email'] == email:
            customer['is_deleted'] = True
            customer['updated_at'] = datetime.now().isoformat()
            save_customers(customers)
            return 'Customer archived.'
    return 'Customer not found.'

def get_revenue_report(customers):
    active = [c for c in customers if not c.get('is_deleted')]
    vips = [c for c in active if c['status'] == 'VIP']
    return {
        'Total Active Leads': len(active),
        'VIP Count': len(vips),
        'Conversion Rate': f'{(len(vips)/len(active)*100 if active else 0):.2f}%'
    }

def main_menu():
    print('
--- CRM V5 REVOPS ENGINE ---')
    customers = load_customers()
    user_input = input('Enter Role (Admin/Reader): ').strip().capitalize()
    role = user_input if user_input in ['Admin', 'Reader'] else 'Reader'
    print(f'Session Started as: {role}')
    while True:
        print('
1. Add Lead (Admin Only)')
        print('2. Search/List Leads')
        print('3. Upgrade to VIP (Admin Only)')
        print('4. Soft Delete Lead (Admin Only)')
        print('5. Revenue Report')
        print('6. Exit')
        choice = input('Select Option: ')
        if choice == '1':
            name, status, email, phone = input('Name: '), input('Status: '), input('Email: '), input('Phone: ')
            print(add_customer(customers, name, status, email, phone, role))
        elif choice == '2':
            query = input('Search: ')
            results = search_customers(customers, query)
            for r in results:
                print(f'[{r["status"]}] {r["name"]} - {r["email"]}')
        elif choice == '3':
            email = input('Email: ')
            print(upgrade_customer(customers, email, role))
        elif choice == '4':
            email = input('Email: ')
            print(soft_delete_customer(customers, email, role))
        elif choice == '5':
            report = get_revenue_report(customers)
            for k, v in report.items(): print(f"{k}: {v}")
        elif choice == '6':
            break

if __name__ == "__main__":
    main_menu()
