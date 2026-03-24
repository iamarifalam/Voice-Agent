from fastapi.testclient import TestClient

from voice_agent_app.main import app


client = TestClient(app)


def test_voice_session_and_response_flow() -> None:
    session_response = client.post(
        "/api/session",
        json={"caller_name": "Ava Patel", "phone_number": "+919000010000"},
    )
    assert session_response.status_code == 200
    session_id = session_response.json()["session_id"]

    response = client.post(
        "/api/respond",
        json={"session_id": session_id, "transcript": "Where is my order right now?"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"] == "order_status"
    assert payload["sources"]


def test_frustrated_caller_escalates() -> None:
    session_response = client.post(
        "/api/session",
        json={"caller_name": "Raj", "phone_number": "+919000010001"},
    )
    session_id = session_response.json()["session_id"]
    response = client.post(
        "/api/respond",
        json={"session_id": session_id, "transcript": "I am angry and want a manager now"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["escalation_required"] is True
    assert payload["intent"] == "escalate"


def test_twilio_voice_webhook_returns_twiml() -> None:
    response = client.post("/webhooks/twilio/voice")
    assert response.status_code == 200
    assert "<Gather" in response.text


def test_dashboard_endpoint_reflects_sessions() -> None:
    session_response = client.post(
        "/api/session",
        json={"caller_name": "Mia", "phone_number": "+919000010099"},
    )
    session_id = session_response.json()["session_id"]
    client.post(
        "/api/respond",
        json={"session_id": session_id, "transcript": "I need a return for a damaged item"},
    )

    response = client.get("/api/dashboard")
    assert response.status_code == 200
    payload = response.json()
    assert payload["active_sessions"] >= 1
    assert payload["knowledge_articles"] >= 3
    assert payload["recent_sessions"]
