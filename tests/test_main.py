
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert "message" in response.json()


def test_about_endpoint():
    response = client.get("/about")

    assert response.status_code == 200
    assert response.json()["developer"] == "Captain Morgan"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["api"] == "Running"


def test_empty_question_is_rejected():
    response = client.post(
        "/ask",
        json={"question": ""}
    )

    assert response.status_code == 422


def test_whitespace_question_is_rejected():
    response = client.post(
        "/ask",
        json={"question": "   "}
    )

    assert response.status_code == 422


def test_question_over_1000_characters_is_rejected():
    response = client.post(
        "/ask",
        json={"question": "a" * 1001}
    )

    assert response.status_code == 422



from unittest.mock import patch


def test_ask_returns_answer_and_sources():
    mock_result = {
        "question": "How do I register a tenant?",
        "answer": "Open Tenants, select Add Tenant, and save the details.",
        "sources": [
            {
                "document": "tenant_manual.txt",
                "section": "TENANT REGISTRATION"
            }
        ]
    }

    with patch("app.main.ask_question", return_value=mock_result):
        response = client.post(
            "/ask",
            json={"question": "How do I register a tenant?"}
        )

    assert response.status_code == 200
    assert response.json()["answer"] == mock_result["answer"]
    assert response.json()["sources"] == mock_result["sources"]


def test_ask_returns_503_when_ai_is_unavailable():
    with patch(
        "app.main.ask_question",
        side_effect=RuntimeError("AI service is currently unavailable.")
    ):
        response = client.post(
            "/ask",
            json={"question": "How do I register a tenant?"}
        )

    assert response.status_code == 503
    assert response.json()["detail"] == "AI service is currently unavailable."
