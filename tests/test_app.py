import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Ensure not already signed up
    client.post(f"/activities/{activity}/unregister", json={"email": email})
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Try signing up again (should fail)
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400


def test_unregister_participant():
    email = "removeme@mergington.edu"
    activity = "Programming Class"
    # Sign up first
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/unregister", json={"email": email})
    assert response.status_code == 200
    assert f"Unregistered {email} from {activity}" in response.json()["message"]
    # Try unregistering again (should fail)
    response2 = client.post(f"/activities/{activity}/unregister", json={"email": email})
    assert response2.status_code == 400


def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404


def test_unregister_invalid_activity():
    response = client.post("/activities/Nonexistent/unregister", json={"email": "test@mergington.edu"})
    assert response.status_code == 404
