import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'


# New Tests for URL Shortener

def test_shorten_url_success(client):
    response = client.post("/api/shorten", json={"url": "https://example.com"})
    assert response.status_code == 200
    data = response.get_json()
    assert "short_code" in data
    assert "short_url" in data

def test_shorten_invalid_url(client):
    response = client.post("/api/shorten", json={"url": "invalid-url"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_redirect_url(client):
    resp = client.post("/api/shorten", json={"url": "https://example.com"})
    short_code = resp.get_json()["short_code"]
    redirect_resp = client.get(f"/{short_code}")
    assert redirect_resp.status_code == 302

def test_redirect_invalid_code(client):
    response = client.get("/xyz999")
    assert response.status_code == 404

def test_stats_endpoint(client):
    resp = client.post("/api/shorten", json={"url": "https://example.com"})
    short_code = resp.get_json()["short_code"]

    # Trigger 2 clicks
    client.get(f"/{short_code}")
    client.get(f"/{short_code}")

    stats_resp = client.get(f"/api/stats/{short_code}")
    assert stats_resp.status_code == 200
    data = stats_resp.get_json()
    assert data["clicks"] == 2
    assert data["url"] == "https://example.com"
    assert "created_at" in data
