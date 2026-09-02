from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "python-data-api",
    }


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Python Data Processing API",
        "documentation": "/docs",
    }


def test_invalid_quantity():
    payload = {
        "product_name": "Keyboard",
        "category": "Electronics",
        "quantity": 0,
        "unit_price": 2500,
        "customer_name": "Test User",
        "region": "South",
    }

    response = client.post("/records", json=payload)

    assert response.status_code == 422


def test_empty_batch():
    response = client.post("/records/batch", json=[])

    assert response.status_code == 400
    assert response.json()["detail"] == "At least one sales record is required"
