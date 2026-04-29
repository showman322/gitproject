import csv
import json
import re
from pathlib import Path
from typing import Optional

from connect import connect  # Function to connect to the database

# Base directory where the script is located
BASE_DIR = Path(__file__).resolve().parent

# Regex pattern for phone validation (+ optional, 6-15 digits)
PHONE_RE = re.compile(r"\+?\d{6,15}$")

# Allowed phone types
PHONE_TYPES = {"home", "work", "mobile"}

# Allowed sorting fields
SORT_FIELDS = {"name", "birthday", "date"}

# Create database connection and cursor
conn = connect()
cur = conn.cursor()


# Executes SQL file (schema or procedures)
def execute_sql_file(filename: str):
    path = BASE_DIR / filename  # Build path to file
    if not path.exists():
        print(f"File not found near phonebook.py: {filename}")
        return
    cur.execute(path.read_text(encoding="utf-8"))  # Execute SQL content
    conn.commit()
    print(f"Executed {path.name}")


# Initializes database structure and procedures
def init_db():
    execute_sql_file("schema.sql")
    execute_sql_file("procedures.sql")


# Validates phone number format
def is_valid_phone(phone: str) -> bool:
    return bool(PHONE_RE.fullmatch(phone.strip()))


# Gets group ID, creates group if it doesn't exist
def get_group_id(group_name: str) -> int:
    group_name = (group_name or "Other").strip() or "Other"

    # Insert group if not exists
    cur.execute(
        "INSERT INTO public.groups(name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (group_name,),
    )

    # Get group ID
    cur.execute(
        "SELECT id FROM public.groups WHERE lower(name) = lower(%s)",
        (group_name,),
    )
    return cur.fetchone()[0]


# Checks if contact already exists
def contact_exists(name: str) -> bool:
    cur.execute(
        "SELECT 1 FROM public.contacts WHERE lower(name) = lower(%s)",
        (name,),
    )
    return cur.fetchone() is not None


# Inserts or updates contact (UPSERT logic)
def upsert_contact(name: str, email: Optional[str], birthday: Optional[str], group_name: str, overwrite: bool = True):
    group_id = get_group_id(group_name)

    if contact_exists(name):
        if overwrite:
            # Update existing contact
            cur.execute("""
                UPDATE public.contacts
                SET email = %s, birthday = NULLIF(%s, '')::DATE, group_id = %s
                WHERE lower(name) = lower(%s)
                RETURNING id
            """, (email or None, birthday or "", group_id, name))
            return cur.fetchone()[0]

        # Return existing ID without updating
        cur.execute(
            "SELECT id FROM public.contacts WHERE lower(name) = lower(%s)",
            (name,),
        )
        return cur.fetchone()[0]

    # Insert new contact
    cur.execute("""
        INSERT INTO public.contacts(name, email, birthday, group_id)
        VALUES (%s, %s, NULLIF(%s, '')::DATE, %s)
        RETURNING id
    """, (name, email or None, birthday or "", group_id))

    return cur.fetchone()[0]


# Adds or updates phone for a contact
def add_phone_by_id(contact_id: int, phone: str, phone_type: str):
    phone = phone.strip()
    phone_type = phone_type.strip().lower()

    # Validate phone
    if not is_valid_phone(phone):
        raise ValueError("Invalid phone number. Use 6-15 digits, optional +.")

    # Validate phone type
    if phone_type not in PHONE_TYPES:
        raise ValueError("Invalid phone type. Use home, work, or mobile.")

    # Insert or update phone
    cur.execute("""
        INSERT INTO public.phones(contact_id, phone, type)
        VALUES (%s, %s, %s)
        ON CONFLICT (contact_id, phone) DO UPDATE SET type = EXCLUDED.type
    """, (contact_id, phone, phone_type))


# Console function to add contact interactively
def add_contact_console():
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    birthday = input("Birthday YYYY-MM-DD or empty: ").strip()
    group_name = input("Group Family/Work/Friend/Other: ").strip() or "Other"

    contact_id = upsert_contact(name, email, birthday, group_name, overwrite=True)

    # Add multiple phones
    while True:
        phone = input("Phone or empty to finish: ").strip()
        if not phone:
            break
        phone_type = input("Type home/work/mobile: ").strip().lower() or "mobile"
        try:
            add_phone_by_id(contact_id, phone, phone_type)
        except ValueError as e:
            print(e)

    conn.commit()
    print("Contact saved.")


# Prints contact rows nicely
def print_rows(rows):
    if not rows:
        print("No records found.")
        return

    for row in rows:
        print("-" * 80)
        print(f"ID: {row[0]} | Name: {row[1]} | Email: {row[2] or ''}")
        print(f"Birthday: {row[3] or ''} | Group: {row[4] or ''} | Created: {row[6]}")
        print(f"Phones: {row[5] or ''}")


# Gets contacts with pagination and sorting
def get_contacts(limit=1000, offset=0, sort_by="name", group_name=None):
    if sort_by not in SORT_FIELDS:
        sort_by = "name"

    cur.execute(
        "SELECT * FROM public.get_contacts_page(%s::INTEGER, %s::INTEGER, %s::TEXT, %s::TEXT)",
        (limit, offset, sort_by, group_name),
    )
    return cur.fetchall()


# Shows all contacts
def show_all(sort_by: str = "name", group_name: Optional[str] = None):
    print_rows(get_contacts(1000, 0, sort_by, group_name))


# Filters contacts by group
def filter_by_group():
    show_all("name", input("Group name: ").strip())


# Search contacts by email
def search_by_email():
    email_query = input("Email search text: ").strip()
    cur.execute("SELECT * FROM public.search_contacts(%s::TEXT)", (email_query,))
    rows = [r for r in cur.fetchall() if email_query.lower() in (r[2] or "").lower()]
    print_rows(rows)


# Search across all fields
def search_all_fields():
    query = input("Search text: ").strip()
    cur.execute("SELECT * FROM public.search_contacts(%s::TEXT)", (query,))
    print_rows(cur.fetchall())


# Pagination navigation in console
def paginated_navigation():
    limit = int(input("Page size: ") or "5")
    sort_by = input("Sort by name/birthday/date: ").strip().lower() or "name"

    if sort_by not in SORT_FIELDS:
        sort_by = "name"

    group_name = input("Filter group or empty: ").strip() or None
    offset = 0

    while True:
        rows = get_contacts(limit, offset, sort_by, group_name)
        print(f"\nPage {(offset // limit) + 1}")
        print_rows(rows)

        cmd = input("next / prev / quit: ").strip().lower()
        if cmd in {"next", "n"} and rows:
            offset += limit
        elif cmd in {"prev", "p"}:
            offset = max(0, offset - limit)
        elif cmd in {"quit", "q"}:
            break


# Calls stored procedure to add phone
def add_phone_console():
    try:
        cur.execute("CALL public.add_phone(%s, %s, %s)", (
            input("Contact name: ").strip(),
            input("New phone: ").strip(),
            input("Type home/work/mobile: ").strip().lower(),
        ))
        conn.commit()
        print("Phone added.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)


# Calls stored procedure to move contact to another group
def move_to_group_console():
    try:
        cur.execute("CALL public.move_to_group(%s, %s)", (
            input("Contact name: ").strip(),
            input("New group: ").strip(),
        ))
        conn.commit()
        print("Contact moved.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)


# Deletes contact
def delete_contact():
    name = input("Contact name to delete: ").strip()
    cur.execute("DELETE FROM public.contacts WHERE lower(name) = lower(%s)", (name,))
    conn.commit()
    print("Deleted if existed.")


# Main menu
def menu():
    init_db()

    while True:
        print("""
--- TSIS 1 PHONEBOOK ---
1. Add/update contact
2. Show all contacts
3. Filter by group
4. Search by email
5. Search all fields
6. Sort results
7. Paginated navigation
8. Add phone procedure
9. Move to group procedure
10. Export to JSON
11. Import from JSON
12. Import from CSV
13. Delete contact
0. Exit
""")
        choice = input("Choose: ").strip()

        if choice == "1": add_contact_console()
        elif choice == "2": show_all()
        elif choice == "3": filter_by_group()
        elif choice == "4": search_by_email()
        elif choice == "5": search_all_fields()
        elif choice == "6": show_all(input("Sort by name/birthday/date: ").strip().lower())
        elif choice == "7": paginated_navigation()
        elif choice == "8": add_phone_console()
        elif choice == "9": move_to_group_console()
        elif choice == "10": pass
        elif choice == "11": pass
        elif choice == "12": pass
        elif choice == "13": delete_contact()
        elif choice == "0": break
        else: print("Invalid choice.")

    cur.close()
    conn.close()


if __name__ == "__main__":
    menu()