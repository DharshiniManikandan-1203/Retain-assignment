import pytest
from app.main import app
from app.database import init_db, get_db_connection
import bcrypt
import uuid




@pytest.fixture
def client():
    init_db()
    app.testing = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["message"] == "User Management API is running!"

def test_create_user_and_password_hashed(client):
    random_email = f"alice-{uuid.uuid4().hex}@example.com"
    new_user = {
        "name": "Alice",
        "email": random_email,
        "password": "mypassword"
    }

    response = client.post("/users", json=new_user)
    assert response.status_code == 201

    # Check if password is hashed in DB
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE email = ?", (new_user["email"],))
    row = cursor.fetchone()

    assert row is not None
    assert row["password"] != new_user["password"]
    assert bcrypt.checkpw(new_user["password"].encode(), row["password"].encode())

    # delete the test user
    cursor.execute("DELETE FROM users WHERE email = ?", (new_user["email"],))
    conn.commit()
    conn.close()


    # Check if password is hashed in DB
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (new_user["email"],))
    row = cursor.fetchone()
    conn.close()

    assert row is not None
    assert row["password"] != new_user["password"]  # Confirm not plain text
    assert bcrypt.checkpw(new_user["password"].encode(), row["password"].encode())

def test_login_user_success(client):
    # Already seeded with john@example.com / password123
    response = client.post("/login", json={"email": "alice@example.com", "password": "password123"})
    assert response.status_code == 200
    data = response.get_json()
    assert "user_id" in data["data"]
    assert data["message"] == "Login successful"

def test_login_user_fail_wrong_password(client):
    response = client.post("/login", json={"email": "alice@example.com", "password": "wrongpass"})
    assert response.status_code == 401
    assert response.get_json()["message"] == "Invalid credentials"


