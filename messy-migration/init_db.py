import bcrypt
from app.database import get_db_connection, init_db

def seed_users():
    users = [
        ("John Doe", "john@example.com", "password123"),
        ("Jane Smith", "jane@example.com", "secret456"),
        ("Bob Johnson", "bob@example.com", "qwerty789")
    ]

    conn = get_db_connection()
    cursor = conn.cursor()

    for name, email, password in users:
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                        (name, email, hashed_pw.decode('utf-8')))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    seed_users()
    print("Database initialized with sample data (passwords hashed).")
