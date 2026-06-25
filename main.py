from crm.database import init_db
from crm.auth import has_permission
from crm.leads import add_lead, get_leads, soft_delete, restore_lead
from crm.reports import get_dashboard

def main():
    init_db()
    print("
--- CRM V5 PRO ENGINE (MODULAR) ---")
    role = input("Role (Admin/Sales/Viewer): ").strip().capitalize()
    
    while True:
        print("
1. Add Lead  2. Search  3. Delete  4. Restore  5. Dashboard  6. Exit")
        choice = input("Select: ")
        
        if choice == "1" and has_permission(role, "create"):
            print(add_lead(input("Name: "), input("Status: "), input("Email: "), input("Phone: ")))
        elif choice == "2" and has_permission(role, "view"):
            results = get_leads(input("Query: "))
            for l in results: print(f"[ID:{l[0]}] {l[1]} ({l[3]}) - Status: {l[2]}")
        elif choice == "3" and has_permission(role, "delete"):
            print(soft_delete(input("Email: ")))
        elif choice == "4" and has_permission(role, "restore"):
            print(restore_lead(input("Email: ")))
        elif choice == "5":
            db = get_dashboard()
            print("
--- PIPELINE REPORT ---")
            for stage, count in db['pipeline']: print(f"{stage}: {count}")
            print(f"Archived Leads: {db['deleted_count']}")
        elif choice == "6": break

if __name__ == "__main__":
    main()
