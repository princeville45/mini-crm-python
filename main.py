from crm.database import init_db
from crm.auth import has_permission
from crm.leads import add_lead, search_leads, soft_delete, restore_lead
from crm.reports import get_dashboard
from crm.config import VALID_STATUSES

def main():
    init_db()
    print("\n--- CRM V5 PRO: ARCHITECTURAL MASTERPIECE ---")
    role = input("Enter Role: ")
    
    actions = {
        "1": lambda r: print(add_lead(input("Name: "), input(f"Status {VALID_STATUSES}: "), input("Email: "), input("Phone: "))),
        "2": lambda r: [print(f"ID:{l[0]} | {l[1]} | {l[2]}") for l in search_leads(input("Search: "))],
        "3": lambda r: print(soft_delete(input("Email to archive: "))) if has_permission(r, "delete") else print("Denied"),
        "4": lambda r: print(restore_lead(input("Email to restore: "))) if has_permission(r, "restore") else print("Denied"),
        "5": lambda r: print(get_dashboard()),
    }

    while True:
        print("\n1.Add 2.Search 3.Archive 4.Restore 5.Stats 6.Exit")
        c = input(">> ")
        if c == "6": break
        if c in actions: actions[c](role)

if __name__ == "__main__": main()
