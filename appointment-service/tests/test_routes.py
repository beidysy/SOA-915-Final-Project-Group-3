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

def test_create_appointment(test_client):
    with requests_mock.Mocker() as m:
        # ✅ Mock patient service with expected header
        m.get(
            "http://patient-service:5001/patients/1",
            request_headers={"X-Patient-ID": "1"},
            json={"id": 1, "name": "Test Patient", "email": "test@example.com"}
        )

        # ✅ Mock doctor service
        m.get(
            "http://doctor-service:5002/doctors/1",
            json={"id": 1, "name": "Dr. Smith", "email": "dr@example.com"}
        )

        # ✅ Mock notification service
        m.post(
            "http://notification-service:5004/notifications",
            json={"message": "Notification sent successfully"}
        )

        # ✅ Send request with correct X-Patient-ID header
        response = test_client.post(
            "/appointments",
            headers={"X-Patient-ID": "1"},
            json={
                "patient_id": 1,
                "doctor_id": 1,
                "date": "2025-06-01",
                "time": "10:00 AM",
                "status": "Scheduled"
            }
        )

        assert response.status_code == 201
        assert response.json["message"] == "Appointment created successfully"

