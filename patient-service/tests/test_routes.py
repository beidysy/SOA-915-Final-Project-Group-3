import pytest
from app import create_app, db
from app.models import Patient

@pytest.fixture
def test_client():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    }

    app = create_app(test_config)

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_create_patient(test_client):
    response = test_client.post("/patients", json={
        "name": "Test Patient",
        "age": 30,
        "email": "test@example.com",
        "phone": "1234567890"
    })
    
    assert response.status_code == 201
    assert b"Patient created successfully" in response.data

