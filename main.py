import sqlite3
import re

def create_table(cursor):
    """Creates the 'users' table if it doesn't already exist."""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT NOT NULL UNIQUE,
            other_data TEXT
        )
    ''')

def validate_email(email):
    """Validates an email address format."""
    # Basic regex for email validation
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def get_user_input():
    """Prompts the user for their details and returns them."""
    name = input("Enter your name: ")
    while not name.strip():
        print("Name cannot be empty.")
        name = input("Enter your name: ")

    age = None
    while age is None:
        try:
            age_str = input("Enter your age: ")
            if age_str.strip(): # Age is optional, but if entered, must be valid
                age = int(age_str)
                if age <= 0:
                    print("Age must be a positive number.")
                    age = None
            else:
                age = None # Allow empty age
        except ValueError:
            print("Invalid age. Please enter a number or leave it empty.")
            age = None

    email = input("Enter your email: ")
    while not validate_email(email):
        print("Invalid email format. Please try again.")
        email = input("Enter your email: ")

    other_data = input("Enter any other data (optional): ")

    return name, age, email, other_data if other_data.strip() else None

def save_user_to_db(name, age, email, other_data, cursor, conn):
    """Saves user data to the database."""
    try:
        cursor.execute(
            "INSERT INTO users (name, age, email, other_data) VALUES (?, ?, ?, ?)",
            (name, age, email, other_data)
        )
        conn.commit()
        print("User data saved successfully!")
    except sqlite3.IntegrityError:
        print(f"Error: A user with the email '{email}' already exists.")
    except Exception as e:
        print(f"An error occurred while saving: {e}")

def main():
    db_name = 'user_data.db'
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        create_table(cursor)

        print("Please provide the following information:")
        name, age, email, other_data = get_user_input()

        save_user_to_db(name, age, email, other_data, cursor, conn)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()
