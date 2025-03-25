from flask import Blueprint, request, jsonify
from app.database import db
from app.models import Notification
import requests

notification_blueprint = Blueprint("notification", __name__, url_prefix="/notifications")

@notification_blueprint.route("", methods=["POST"])
def create_notification():
    data = request.get_json()

    # Validate if the appointment exists
    appointment_response = requests.get(f"http://appointment-service:5003/appointments/{data['appointment_id']}")

    if appointment_response.status_code != 200:
        return jsonify({"error": "Appointment does not exist"}), 400

    # Store notification in the database
    new_notification = Notification(
        appointment_id=data["appointment_id"],
        message=data["message"],
        status="Pending"
    )
    db.session.add(new_notification)
    db.session.commit()

    # 🔔 Send notification to the patient
    appointment_data = appointment_response.json()
    patient_id = appointment_data["patient_id"]
    
    # Get patient details
    # Get patient details using RBAC header
    headers = {"X-Patient-ID": str(patient_id)}
    patient_response = requests.get(
        f"http://patient-service:5001/patients/{patient_id}",
        headers=headers
    )


    if patient_response.status_code != 200:
        return jsonify({"error": "Patient not found, notification not sent"}), 400

    patient_data = patient_response.json()
    patient_email = patient_data["email"]

    # Simulate sending email
    print(f"📧 Sending email to {patient_email}: {data['message']}")

    # Update notification status to "Sent"
    new_notification.status = "Sent"
    db.session.commit()

    return jsonify({"message": "Notification sent successfully"}), 201

@notification_blueprint.route("", methods=["GET"])
def get_notifications():
    notifications = Notification.query.all()
    return jsonify([
        {
            "id": n.id,
            "appointment_id": n.appointment_id,
            "message": n.message,
            "status": n.status,
            "created_at": str(n.created_at)
        }
        for n in notifications
    ])

@notification_blueprint.route("/<int:id>", methods=["GET"])
def get_notification(id):
    notification = Notification.query.get_or_404(id)
    return jsonify({
        "id": notification.id,
        "appointment_id": notification.appointment_id,
        "message": notification.message,
        "status": notification.status,
        "created_at": str(notification.created_at)
    })

@notification_blueprint.route("/<int:id>", methods=["PUT"])
def update_notification(id):
    data = request.get_json()
    notification = Notification.query.get_or_404(id)
    notification.status = data.get("status", notification.status)
    db.session.commit()
    return jsonify({"message": "Notification updated successfully"})

@notification_blueprint.route("/<int:id>", methods=["DELETE"])
def delete_notification(id):
    notification = Notification.query.get_or_404(id)
    db.session.delete(notification)
    db.session.commit()
    return jsonify({"message": "Notification deleted successfully"})

@notification_blueprint.route("/patient/<int:patient_id>", methods=["GET"])
def get_notifications_for_patient(patient_id):
    # Fetch all appointments for this patient
    appointment_response = requests.get(f"http://appointment-service:5003/appointments")
    
    if appointment_response.status_code != 200:
        return jsonify({"error": "Could not fetch appointments"}), 400

    appointments = appointment_response.json()
    patient_appointments = [a["id"] for a in appointments if a["patient_id"] == patient_id]

    if not patient_appointments:
        return jsonify({"message": "No notifications found for this patient"}), 200

    # Fetch notifications related to the patient's appointments
    notifications = Notification.query.filter(Notification.appointment_id.in_(patient_appointments)).all()

    return jsonify([
        {
            "id": n.id,
            "appointment_id": n.appointment_id,
            "message": n.message,
            "status": n.status,
            "created_at": str(n.created_at)
        }
        for n in notifications
    ])

