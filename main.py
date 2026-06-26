import logging
from crm.database import init_db
from crm.auth import has_permission
from crm.leads import add_lead, get_leads, soft_delete, restore_lead, VALID_STATUSES
from crm.reports import get_dashboard

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def collect_lead_input():
    """Decoupled input collection as recommended by coach."""
    return {
        "name": input("Name: "),
        "status": input(f"Status {VALID_STATUSES}: "),
        "email": input("Email: "),
        "phone": input("Phone: ")
    }

def handle_add(role):
    if has_permission(role, "create"):
        data = collect_lead_input()
        print(add_lead(**data))
    else:
        print("Access Denied.")

def handle_search(role):
    if has_permission(role, "view"):
        q = input("Search: ")
        s = input("Status Filter (Enter to skip): ")
        results = get_leads(query=q, status=s)
        for l in results: print(f"[ID:{l[0]}] {l[1]} ({l[3]}) | Status: {l[2]}")
    else:
        print("Access Denied.")

def handle_archive(role):
    if has_permission(role, "delete"):
        print(soft_delete(input("Email: ")))
    else:
        print("Access Denied.")

def handle_restore(role):
    if has_permission(role, "restore"):
        print(restore_lead(input("Email: ")))
    else:
        print("Access Denied.")

def handle_dashboard(role):
    db = get_dashboard()
    print("\n--- PIPELINE ---")
    for s, c in db['pipeline']: print(f"{s}: {c}")
    print("\n--- HOT LEADS ---")
    for name, score in db['hot_leads']: print(f"{name}: {score} interactions")

def main():
    init_db()
    logger.info("CRM V5 PRO Started.")
    role = input("Role (Admin/Sales/Viewer): ").strip().capitalize()
    
    # Menu Mapping (Refactored from if/elif as recommended)
    MENU_ACTIONS = {
        "1": handle_add,
        "2": handle_search,
        "3": handle_archive,
        "4": handle_restore,
        "5": handle_dashboard
    }

    while True:
        print("\n1. Add Lead | 2. Search | 3. Archive | 4. Restore | 5. Dashboard | 6. Exit")
        choice = input("Select: ")
        
        if choice == "6": 
            logger.info("CRM Closed.")
            break
            
        action = MENU_ACTIONS.get(choice)
        if action:
            action(role)
        else:
            print("Invalid Choice.")

if __name__ == "__main__":
    main()
