import csv
from connect import connect

# Create a connection and cursor to work with the database
conn = connect()
cur = conn.cursor()


def create_table():
    """
    Create the phonebook table if it does not already exist.
    The table contains:
    - id (primary key)
    - name (string, required)
    - phone (string, required, must be unique)
    """
    cur.execute("""
        CREATE TABLE IF NOT EXISTS public.phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL UNIQUE
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
    """
    Insert a new contact into the phonebook using user input.
    """
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    cur.execute(
        "INSERT INTO public.phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    print("Contact added successfully.")


def insert_from_csv():
    """
    Insert multiple contacts from a CSV file.
    Each row must contain at least: name, phone.
    Duplicate phone numbers are ignored due to ON CONFLICT.
    """
    filename = input("Enter CSV file name: ")

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            # Ensure the row has at least 2 columns
            if len(row) >= 2:
                name = row[0]
                phone = row[1]

                cur.execute(
                    """
                    INSERT INTO public.phonebook (name, phone)
                    VALUES (%s, %s)
                    ON CONFLICT (phone) DO NOTHING
                    """,
                    (name, phone)
                )

    conn.commit()
    print("Data imported from CSV.")


def update_contact():
    """
    Update either the name or phone number of an existing contact.
    """
    print("What do you want to update?")
    print("1 - Update name")
    print("2 - Update phone")

    choice = input("Choose: ")

    if choice == "1":
        old_name = input("Enter current name: ")
        new_name = input("Enter new name: ")

        cur.execute(
            "UPDATE public.phonebook SET name = %s WHERE name = %s",
            (new_name, old_name)
        )
        conn.commit()
        print("Name updated successfully.")

    elif choice == "2":
        name = input("Enter contact name: ")
        new_phone = input("Enter new phone: ")

        cur.execute(
            "UPDATE public.phonebook SET phone = %s WHERE name = %s",
            (new_phone, name)
        )
        conn.commit()
        print("Phone updated successfully.")

    else:
        print("Invalid choice.")


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


def query_by_name():
    """
    Search contacts by name (case-insensitive, partial match).
    """
    name = input("Enter name to search: ")

    cur.execute(
        "SELECT * FROM public.phonebook WHERE name ILIKE %s",
        ('%' + name + '%',)
    )
    rows = cur.fetchall()

    if len(rows) == 0:
        print("No contacts found.")
    else:
        for row in rows:
            print(row)


def query_by_phone_prefix():
    """
    Search contacts by phone number prefix.
    """
    prefix = input("Enter phone prefix: ")

    cur.execute(
        "SELECT * FROM public.phonebook WHERE phone LIKE %s",
        (prefix + '%',)
    )
    rows = cur.fetchall()

    if len(rows) == 0:
        print("No contacts found.")
    else:
        for row in rows:
            print(row)


def delete_contact():
    """
    Delete a contact either by name or by phone number.
    """
    print("Delete contact by:")
    print("1 - Name")
    print("2 - Phone")

    choice = input("Choose: ")

    if choice == "1":
        name = input("Enter name: ")

        cur.execute(
            "DELETE FROM public.phonebook WHERE name = %s",
            (name,)
        )
        conn.commit()
        print("Contact deleted successfully.")

    elif choice == "2":
        phone = input("Enter phone: ")

        cur.execute(
            "DELETE FROM public.phonebook WHERE phone = %s",
            (phone,)
        )
        conn.commit()
        print("Contact deleted successfully.")

    else:
        print("Invalid choice.")


def menu():
    """
    Main menu loop for interacting with the phonebook.
    """
    check_connection()
    create_table()

    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Insert contact from console")
        print("2. Insert contacts from CSV")
        print("3. Update contact")
        print("4. Show all contacts")
        print("5. Search contacts by name")
        print("6. Search contacts by phone prefix")
        print("7. Delete contact")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            insert_from_console()
        elif choice == "2":
            insert_from_csv()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            query_all_contacts()
        elif choice == "5":
            query_by_name()
        elif choice == "6":
            query_by_phone_prefix()
        elif choice == "7":
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