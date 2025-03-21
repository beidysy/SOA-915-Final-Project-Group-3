from flask import Blueprint, request, jsonify
from app.database import db
from app.models import Appointment
import requests

appointment_blueprint = Blueprint("appointment", __name__, url_prefix="/appointments")



@appointment_blueprint.route("", methods=["POST"])
def create_appointment():
    data = request.get_json()

    # Validate if the patient and doctor exist
    #patient_response = requests.get(f"http://127.0.0.1:5001/patients/{data['patient_id']}")
    #doctor_response = requests.get(f"http://127.0.0.1:5002/doctors/{data['doctor_id']}")
    patient_response = requests.get(f"http://patient-service:5001/patients/{data['patient_id']}")
    doctor_response = requests.get(f"http://doctor-service:5002/doctors/{data['doctor_id']}")


    if patient_response.status_code != 200:
        return jsonify({"error": "Patient does not exist"}), 400

    if doctor_response.status_code != 200:
        return jsonify({"error": "Doctor does not exist"}), 400

    # Create appointment
    new_appointment = Appointment(
        patient_id=data["patient_id"],
        doctor_id=data["doctor_id"],
        date=data["date"],
        time=data["time"],
        status=data.get("status", "Scheduled")
    )
    db.session.add(new_appointment)
    db.session.commit()

    # 🔔 Send notification request to Notification Service
    notification_data = {
        "appointment_id": new_appointment.id,
        "message": f"Your appointment with Doctor {data['doctor_id']} is scheduled for {data['date']} at {data['time']}."
    }
    #requests.post("http://127.0.0.1:5004/notifications", json=notification_data)
    requests.post("http://notification-service:5004/notifications", json=notification_data)


    return jsonify({"message": "Appointment created successfully"}), 201


@appointment_blueprint.route("", methods=["GET"])
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify([
        {"id": a.id, "patient_id": a.patient_id, "doctor_id": a.doctor_id, "date": a.date, "time": a.time, "status": a.status} 
        for a in appointments
    ])

@appointment_blueprint.route("/<int:id>", methods=["GET"])
def get_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    return jsonify({
        "id": appointment.id,
        "patient_id": appointment.patient_id,
        "doctor_id": appointment.doctor_id,
        "date": appointment.date,
        "time": appointment.time,
        "status": appointment.status
    })

@appointment_blueprint.route("/<int:id>", methods=["PUT"])
def update_appointment(id):
    data = request.get_json()
    appointment = Appointment.query.get_or_404(id)
    appointment.date = data.get("date", appointment.date)
    appointment.time = data.get("time", appointment.time)
    appointment.status = data.get("status", appointment.status)
    db.session.commit()
    return jsonify({"message": "Appointment updated successfully"})

@appointment_blueprint.route("/<int:id>", methods=["DELETE"])
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    db.session.delete(appointment)
    db.session.commit()
    return jsonify({"message": "Appointment deleted successfully"})

