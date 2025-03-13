import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure SQLite Database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "notifications.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define Notification Model
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, nullable=False)
    patient_name = db.Column(db.String(100), nullable=False)
    doctor_name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default="Sent")

# Create the database tables
with app.app_context():
    db.create_all()

@app.route("/send_notification", methods=["POST"])
def send_notification():
    data = request.get_json()

    # Fetch appointment details
    appointment_response = requests.get(f"http://appointment-service:5003/appointments")
    appointment_data = appointment_response.json()

    # Find the requested appointment
    appointment = next((a for a in appointment_data["appointments"] if a["id"] == data["appointment_id"]), None)
    if not appointment:
        return jsonify({"error": "Invalid appointment_id"}), 400

    patient_id = appointment["patient_id"]
    doctor_id = appointment["doctor_id"]

    # Fetch patient details
    patient_response = requests.get(f"http://patient-service:5001/patients")
    patient_data = patient_response.json()
    patient = next((p for p in patient_data["patients"] if p["id"] == patient_id), None)

    # Fetch doctor details
    doctor_response = requests.get(f"http://doctor-service:5002/doctors")
    doctor_data = doctor_response.json()
    doctor = next((d for d in doctor_data["doctors"] if d["id"] == doctor_id), None)

    if not patient or not doctor:
        return jsonify({"error": "Invalid patient_id or doctor_id"}), 400

    # Create notification message
    message = f"Reminder for {patient['name']}: You have an appointment with {doctor['name']} on {appointment['date']} at {appointment['time']}."

    # Store notification in database
    new_notification = Notification(
        appointment_id=data["appointment_id"],
        patient_name=patient["name"],
        doctor_name=doctor["name"],
        message=message
    )
    db.session.add(new_notification)
    db.session.commit()

    return jsonify({
        "message": "Notification sent successfully!",
        "notification": {
            "id": new_notification.id,
            "appointment_id": new_notification.appointment_id,
            "patient_name": new_notification.patient_name,
            "doctor_name": new_notification.doctor_name,
            "message": new_notification.message,
            "status": new_notification.status
        }
    }), 201

@app.route("/notifications", methods=["GET"])
def get_notifications():
    notifications = Notification.query.all()
    return jsonify({
        "notifications": [
            {
                "id": n.id,
                "appointment_id": n.appointment_id,
                "patient_name": n.patient_name,
                "doctor_name": n.doctor_name,
                "message": n.message,
                "status": n.status
            }
            for n in notifications
        ]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)
