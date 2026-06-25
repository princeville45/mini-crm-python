from crm.database import init_db
from crm.auth import has_permission
from crm.leads import add_lead, get_leads, soft_delete, restore_lead, VALID_STATUSES
from crm.reports import get_dashboard

def main():
    init_db()
    print("
--- CRM V5 PRO: ADVANCED EDITION ---")
    role = input("Role (Admin/Sales/Viewer): ").strip().capitalize()
    while True:
        print("
1. Add Lead  2. Advanced Search  3. Archive  4. Restore  5. Performance Dashboard  6. Exit")
        choice = input("Select: ")
        if choice == "1" and has_permission(role, "create"):
            print(add_lead(input("Name: "), input("Status: "), input("Email: "), input("Phone: ")))
        elif choice == "2" and has_permission(role, "view"):
            results = get_leads(query=input("Search: "), status=input("Status Filter: "))
            for l in results: print(f"[ID:{l[0]}] {l[1]} ({l[3]}) | Status: {l[2]}")
        elif choice == "3" and has_permission(role, "delete"):
            print(soft_delete(input("Email: ")))
        elif choice == "4" and has_permission(role, "restore"):
            print(restore_lead(input("Email: ")))
        elif choice == "5":
            db = get_dashboard()
            print("
--- PIPELINE ---")
            for s, c in db['pipeline']: print(f"{s}: {c}")
            print("
--- HOT LEADS ---")
            for n, sc in db['hot_leads']: print(f"{n}: {sc} interactions")
        elif choice == "6": break

if __name__ == "__main__":
    main()
