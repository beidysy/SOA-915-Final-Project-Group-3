import pytest
from app import create_app, db
from app.models import Doctor

@pytest.fixture
def test_client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        yield app.test_client()

def test_create_doctor(test_client):
    response = test_client.post("/doctors", json={
        "name": "Dr. Test",
        "specialty": "Cardiology",
        "email": "dr.test@example.com",
        "phone": "1234567890"
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "Doctor created successfully"

