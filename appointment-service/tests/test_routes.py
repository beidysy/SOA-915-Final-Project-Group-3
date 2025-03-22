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

    return app.test_client()

def test_create_appointment(test_client):
    with requests_mock.Mocker() as m:
        # ✅ Mock external services
        m.get("http://patient-service:5001/patients/1", json={"id": 1})
        m.get("http://doctor-service:5002/doctors/1", json={"id": 1})
        m.post("http://notification-service:5004/notifications", json={"message": "Notification sent successfully"})

        response = test_client.post("/appointments", json={
            "patient_id": 1,
            "doctor_id": 1,
            "date": "2025-06-01",
            "time": "10:00 AM",
            "status": "Scheduled"
        })

        assert response.status_code == 201
        assert b"Appointment created successfully" in response.data

