from flask import Blueprint, request, jsonify
from app.database import db
from app.models import Patient

patient_blueprint = Blueprint("patient", __name__, url_prefix="/patients")

@patient_blueprint.route("", methods=["POST"])  # Remove trailing slash
def create_patient():
    data = request.get_json()
    new_patient = Patient(name=data["name"], age=data["age"], email=data["email"], phone=data["phone"])
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({"message": "Patient created successfully"}), 201

@patient_blueprint.route("", methods=["GET"])
def get_patients():
    patients = Patient.query.all()
    return jsonify([
        {  
            "id": p.id,
            "name": p.name,
            "age": p.age,
            "phone": p.phone,
            "email": p.email
        }
        for p in patients
    ])

@patient_blueprint.route("/<int:id>", methods=["GET"])
def get_patient(id):
    patient = Patient.query.get_or_404(id)
    return jsonify({ "id": patient.id, "name": patient.name, "age": patient.age, "email": patient.email, "phone": patient.phone })

@patient_blueprint.route("/<int:id>", methods=["PUT"])
def update_patient(id):
    data = request.get_json()
    patient = Patient.query.get_or_404(id)
    patient.name = data.get("name", patient.name)
    patient.age = data.get("age", patient.age)
    patient.email = data.get("email", patient.email)
    patient.phone = data.get("phone", patient.phone)
    db.session.commit()
    return jsonify({"message": "Patient updated successfully"})

@patient_blueprint.route("/<int:id>", methods=["DELETE"])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return jsonify({"message": "Patient deleted successfully"})
    
