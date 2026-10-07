"""
init_db.py — builds the SQLite database for the RED ACCESS challenge.

Run once (the app also auto-runs this on first start if red_access.db
is missing) to create the users table and seed two accounts.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "red_access.db")


def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
        """
    )

    # Seed accounts. The admin password is intentionally unguessable —
    # players are not meant to log in as admin by knowing the password,
    # they're meant to log in as admin by breaking the query.
    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        ("guest", "guest123", "user"),
    )
    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        ("admin", "Tr0ub4dor&3xtr3me!", "admin"),
    )

    conn.commit()
    conn.close()
    print(f"[init_db] Database created at {DB_PATH}")


if __name__ == "__main__":
    init_db()
