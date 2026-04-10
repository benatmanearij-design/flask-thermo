import sqlite3


def create_user(username, email, password):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def check_user(username, password):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()
    return user


def get_user_by_email(email):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    conn.close()
    return user


def update_password_by_email(email, new_password):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET password = ? WHERE email = ?",
        (new_password, email)
    )

    conn.commit()
    conn.close()


def insert_operation(username, x1, x2, P1, P2, P, y1, y2):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO operations (username, x1, x2, P1, P2, P, y1, y2)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (username, x1, x2, P1, P2, P, y1, y2))

    conn.commit()
    conn.close()


def get_history(username):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT x1, x2, P1, P2, P, y1, y2
    FROM operations
    WHERE username = ?
    ORDER BY id DESC
    """, (username,))

    data = cursor.fetchall()
    conn.close()
    return data