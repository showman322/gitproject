from connect import connect
import re

# Create connection and cursor
conn = connect()
cur = conn.cursor()


def create_table():
    """
    Create the phonebook table if it does not already exist.

    We make 'name' UNIQUE because in the new task
    we identify an existing user by name:
    if the name already exists, we update the phone.
    """
    cur.execute("""
        CREATE TABLE IF NOT EXISTS public.phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            phone VARCHAR(20) NOT NULL
        )
    """)
    conn.commit()


def check_connection():
    """
    Check which database we are connected to.
    Useful for debugging connection issues.
    """
    cur.execute("SELECT current_database();")
    print("Connected to DB:", cur.fetchone()[0])


def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ").strip()

    if not re.fullmatch(r"\+?\d{6,15}", phone):
        print("Invalid phone number! Must be 6–15 digits (optional +).")
        return

    cur.execute(
        "CALL public.insert_or_update_user(%s, %s)",
        (name, phone)
    )
    conn.commit()

    print("User inserted or updated successfully.")

def insert_many_users():
    """
    Insert many users from lists of names and phones.

    This function collects data from the console,
    creates two Python lists (names and phones),
    and sends them to the SQL procedure:
    public.insert_many_users(names, phones, wrong_data)

    Note:
    wrong_data is handled inside the PostgreSQL procedure.
    """
    count = int(input("How many users do you want to add? "))

    names = []
    phones = []

    for i in range(count):
        print(f"\nUser {i + 1}")
        name = input("Enter name: ")
        phone = input("Enter phone: ")

        names.append(name)
        phones.append(phone)

    wrong_data = ""

    cur.execute(
        "CALL public.insert_many_users(%s, %s, %s)",
        (names, phones, wrong_data)
    )
    conn.commit()

    print("Many users procedure finished.")
    print("Incorrect phones are processed inside the SQL procedure.")


def query_all_contacts():
    """
    Retrieve and display all contacts sorted by ID.
    """
    cur.execute("SELECT * FROM public.phonebook ORDER BY id")
    rows = cur.fetchall()

    if len(rows) == 0:
        print("PhoneBook is empty.")
    else:
        for row in rows:
            print(row)


def search_by_pattern():
    """
    Search all records matching a pattern.

    This function calls the SQL function:
    public.search_phonebook(pattern_text)

    The pattern can match part of:
    - name
    - phone
    """
    pattern = input("Enter search pattern: ")

    cur.execute(
        "SELECT * FROM public.search_phonebook(%s)",
        (pattern,)
    )
    rows = cur.fetchall()

    if len(rows) == 0:
        print("No matching records found.")
    else:
        for row in rows:
            print(row)


def show_contacts_with_pagination():
    """
    Query data from the table with pagination.

    This function calls the SQL function:
    public.get_phonebook_page(limit, offset)

    LIMIT  - how many rows to return
    OFFSET - how many rows to skip
    """
    limit = int(input("Enter LIMIT: "))
    offset = int(input("Enter OFFSET: "))

    cur.execute(
        "SELECT * FROM public.get_phonebook_page(%s, %s)",
        (limit, offset)
    )
    rows = cur.fetchall()

    if len(rows) == 0:
        print("No records found.")
    else:
        for row in rows:
            print(row)


def delete_contact():
    """
    Delete a contact by username or phone.

    This function calls the SQL procedure:
    public.delete_user(value)
    """
    value = input("Enter username or phone: ")

    cur.execute(
        "CALL public.delete_user(%s)",
        (value,)
    )
    conn.commit()

    print("Contact deleted successfully.")


def menu():
    """
    Main menu loop for interacting with the phonebook.
    """
    check_connection()
    create_table()

    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Insert or update one user")
        print("2. Insert many users")
        print("3. Show all contacts")
        print("4. Search by pattern")
        print("5. Show contacts with pagination")
        print("6. Delete by username or phone")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            insert_from_console()
        elif choice == "2":
            insert_many_users()
        elif choice == "3":
            query_all_contacts()
        elif choice == "4":
            search_by_pattern()
        elif choice == "5":
            show_contacts_with_pagination()
        elif choice == "6":
            delete_contact()
        elif choice == "0":
            print("Program finished.")
            break
        else:
            print("Invalid choice. Try again.")

    # Close database connection properly
    cur.close()
    conn.close()


if __name__ == "__main__":
    menu()