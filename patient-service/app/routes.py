from flask import Blueprint, request, jsonify
from app.database import db
from app.models import Patient
import logging

logger = logging.getLogger(__name__)

patient_blueprint = Blueprint("patient", __name__, url_prefix="/patients")

@patient_blueprint.route("", methods=["POST"])
def create_patient():
    data = request.get_json()
    new_patient = Patient(
        name=data["name"],
        age=data["age"],
        email=data["email"],
        phone=data["phone"]
    )
    db.session.add(new_patient)
    db.session.commit()
    logger.info(f"✅ Created new patient: {new_patient.name} (ID: {new_patient.id})")
    return jsonify({"message": "Patient created successfully"}), 201


@patient_blueprint.route("", methods=["GET"])
def get_patients():
    patients = Patient.query.all()
    logger.info(f"📥 Retrieved all patients. Count: {len(patients)}")
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
    # Simulated authentication using custom header
    authenticated_patient_id = request.headers.get("X-Patient-ID")

    logger.info(f"🔐 Header X-Patient-ID: {authenticated_patient_id}")
    logger.info(f"📦 Requested patient ID: {id}")

    if not authenticated_patient_id:
        logger.warning("🚫 Missing X-Patient-ID header")
        return jsonify({"error": "Missing X-Patient-ID header"}), 401

    try:
        if int(authenticated_patient_id) != id:
            logger.warning("🚫 Unauthorized access attempt")
            return jsonify({"error": "Unauthorized access"}), 403
    except ValueError:
        logger.error("❌ Invalid ID format in header")
        return jsonify({"error": "Invalid ID format in header"}), 400

    patient = Patient.query.get_or_404(id)
    logger.info(f"✅ Patient retrieved: {patient.name} (ID: {id})")
    return jsonify({
        "id": patient.id,
        "name": patient.name,
        "age": patient.age,
        "email": patient.email,
        "phone": patient.phone
    })


@patient_blueprint.route("/<int:id>", methods=["PUT"])
def update_patient(id):
    data = request.get_json()
    patient = Patient.query.get_or_404(id)
    patient.name = data.get("name", patient.name)
    patient.age = data.get("age", patient.age)
    patient.email = data.get("email", patient.email)
    patient.phone = data.get("phone", patient.phone)
    db.session.commit()
    logger.info(f"✏️ Updated patient: {patient.name} (ID: {id})")
    return jsonify({"message": "Patient updated successfully"})


@patient_blueprint.route("/<int:id>", methods=["DELETE"])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    logger.info(f"❌ Deleted patient: {patient.name} (ID: {id})")
    return jsonify({"message": "Patient deleted successfully"})

