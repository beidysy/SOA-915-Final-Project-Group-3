from flask import Blueprint, request, jsonify
from app.database import db
from app.models import Doctor

doctor_blueprint = Blueprint("doctor", __name__, url_prefix="/doctors")

@doctor_blueprint.route("", methods=["POST"])
def create_doctor():
    data = request.get_json()
    new_doctor = Doctor(name=data["name"], specialty=data["specialty"], phone=data["phone"], email=data["email"])
    db.session.add(new_doctor)
    db.session.commit()
    return jsonify({"message": "Doctor created successfully"}), 201

@doctor_blueprint.route("", methods=["GET"])
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify([
        {"id": d.id, "name": d.name, "specialty": d.specialty, "phone": d.phone, "email": d.email} for d in doctors
    ])

@doctor_blueprint.route("/<int:id>", methods=["GET"])
def get_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    return jsonify({"id": doctor.id, "name": doctor.name, "specialty": doctor.specialty, "phone": doctor.phone, "email": doctor.email})

@doctor_blueprint.route("/<int:id>", methods=["PUT"])
def update_doctor(id):
    data = request.get_json()
    doctor = Doctor.query.get_or_404(id)
    doctor.name = data.get("name", doctor.name)
    doctor.specialty = data.get("specialty", doctor.specialty)
    doctor.phone = data.get("phone", doctor.phone)
    doctor.email = data.get("email", doctor.email)
    db.session.commit()
    return jsonify({"message": "Doctor updated successfully"})

@doctor_blueprint.route("/<int:id>", methods=["DELETE"])
def delete_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    db.session.delete(doctor)
    db.session.commit()
    return jsonify({"message": "Doctor deleted successfully"})

