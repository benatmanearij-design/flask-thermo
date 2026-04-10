import sqlite3


def init_db():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS operations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        x1 REAL,
        x2 REAL,
        P1 REAL,
        P2 REAL,
        P REAL,
        y1 REAL,
        y2 REAL
    )
    """)

    conn.commit()
    conn.close()