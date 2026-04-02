from database import get_connection

def insert_operation(x1, x2, P1, P2, P, y1, y2):
    conn = get_connection()
    conn.execute(
        "INSERT INTO history (x1,x2,P1,P2,P,y1,y2) VALUES (?,?,?,?,?,?,?)",
        (x1, x2, P1, P2, P, y1, y2)
    )
    conn.commit()
    conn.close()

def get_history():
    conn = get_connection()
    data = conn.execute("SELECT * FROM history").fetchall()
    conn.close()
    return data