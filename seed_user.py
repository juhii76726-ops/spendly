import os
import random
import string
from datetime import datetime
from werkzeug.security import generate_password_hash

# Ensure the project root is in PYTHONPATH so we can import database.db
project_root = os.path.abspath(os.path.dirname(__file__))
import sys
sys.path.append(project_root)

from database.db import get_db, init_db

# Simple lists of Indian first and last names (representative samples)
FIRST_NAMES = [
    "Aarav", "Aditi", "Arjun", "Bhavna", "Chirag", "Deepika",
    "Gaurav", "Isha", "Karan", "Lakshmi", "Manish", "Neha",
    "Ravi", "Sanjay", "Sneha", "Vikram", "Yash", "Zara"
]
LAST_NAMES = [
    "Sharma", "Patel", "Singh", "Kumar", "Gupta", "Reddy",
    "Desai", "Mehta", "Agarwal", "Nair", "Joshi", "Choudhary",
    "Bhatia", "Dutta", "Iyer", "Mishra", "Verma", "Kapoor"
]

def generate_name():
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    return f"{first} {last}", first.lower(), last.lower()

def generate_email(first, last):
    # 2-3 digit random suffix
    suffix = str(random.randint(10, 999))
    return f"{first}.{last}{suffix}@gmail.com"

def user_exists(conn, email):
    cur = conn.execute('SELECT 1 FROM users WHERE email = ?', (email,))
    return cur.fetchone() is not None

def insert_user(conn, name, email, password_hash, created_at):
    cur = conn.execute(
        'INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)',
        (name, email, password_hash, created_at)
    )
    conn.commit()
    return cur.lastrowid

def main():
    # Ensure tables exist
    init_db()
    conn = get_db()
    # Generate unique user
    while True:
        full_name, first, last = generate_name()
        email = generate_email(first, last)
        if not user_exists(conn, email):
            break
    password_hash = generate_password_hash('password123')
    created_at = datetime.utcnow().isoformat(timespec='seconds')
    user_id = insert_user(conn, full_name, email, password_hash, created_at)
    print(f"-id {user_id}\nname {full_name}\nemail {email}")
    conn.close()

if __name__ == '__main__':
    main()
