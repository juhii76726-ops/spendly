import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

# Path to the SQLite database file placed at the project root
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'spendly.db')


def get_db():
    """Return a SQLite connection with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    """Create tables if they do not exist."""
    conn = get_db()
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    ''')

    # Expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()


def seed_db():
    """Insert sample data for development. Skip if users already exist."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    # Insert demo user
    cursor.execute(
        'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
        ('Demo User', 'demo@spendly.com', generate_password_hash('demo123'))
    )
    user_id = cursor.lastrowid

    # Insert sample expenses
    categories = ['Food', 'Transport', 'Bills', 'Health', 'Entertainment', 'Shopping', 'Other']
    expenses = [
        (user_id, 45.50, 'Food', '2026-06-15', 'Grocery shopping'),
        (user_id, 25.00, 'Transport', '2026-06-14', 'Bus fare'),
        (user_id, 1200.00, 'Bills', '2026-06-10', 'Electricity bill'),
        (user_id, 350.00, 'Health', '2026-06-08', 'Medicine'),
        (user_id, 199.00, 'Entertainment', '2026-06-05', 'Movie tickets'),
        (user_id, 890.00, 'Shopping', '2026-06-03', 'Clothing'),
        (user_id, 75.25, 'Food', '2026-06-01', 'Restaurant dinner'),
        (user_id, 50.00, 'Other', '2026-05-28', 'Miscellaneous'),
    ]

    for expense in expenses:
        cursor.execute(
            'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
            expense
        )

    conn.commit()
    conn.close()