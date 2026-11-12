
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["application"] == "FinSafe AI"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_application_info():
    response = client.get("/api/v1/info")

    assert response.status_code == 200
    assert response.json()["version"] == "0.1.0"


def test_message_analysis():
    response = client.post(
        "/api/v1/analyse/message",
        json={
            "message": "Your bank account will be blocked. Verify immediately.",
            "jurisdiction": "SG",
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_empty_message():
    response = client.post(
        "/api/v1/analyse/message",
        json={"message": ""},
    )

    assert response.status_code == 422


def test_missing_message():
    response = client.post(
        "/api/v1/analyse/message",
        json={},
    )

    assert response.status_code == 422


def test_message_exceeds_maximum_length():
    response = client.post(
        "/api/v1/analyse/message",
        json={"message": "A" * 5001},
    )

    assert response.status_code == 422

def test_analyse_message_detects_financial_transaction_request():
    response = client.post(
        "/api/v1/analyse/message",
        json={
            "message": "Transfer $500 to this account to unlock your funds.",
            "jurisdiction": "Singapore",
        },
    )

    assert response.status_code == 200

    data = response.json()
    categories = [
        indicator["category"]
        for indicator in data["indicators"]
    ]

    assert "transaction_request" in categories
