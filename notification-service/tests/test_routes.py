import pytest
import requests_mock
from app import create_app, db

@pytest.fixture
def test_client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client

def test_create_notification(test_client):
    with requests_mock.Mocker() as m:
        # Mock appointment-service response
        m.get("http://appointment-service:5003/appointments/1", json={
            "id": 1,
            "patient_id": 1,
            "doctor_id": 1,
            "date": "2025-06-01",
            "time": "10:00 AM"
        })

        # Mock patient-service response
        m.get("http://patient-service:5001/patients/1", json={
            "id": 1,
            "name": "Test Patient",
            "email": "test@example.com"
        })

        # POST to /notifications
        response = test_client.post("/notifications", json={
            "appointment_id": 1,
            "message": "Your appointment is confirmed."
        })

        assert response.status_code == 201
        assert response.json["message"] == "Notification sent successfully"


