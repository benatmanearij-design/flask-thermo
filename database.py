import sqlite3

DB_NAME = "app.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            x1 REAL,
            x2 REAL,
            P1 REAL,
            P2 REAL,
            P REAL,
            y1 REAL,
            y2 REAL
        )
    ''')
    conn.commit()
    conn.close()