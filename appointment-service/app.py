from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure SQLite Database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "appointments.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define Appointment Model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    doctor_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default="Scheduled")

# Create the database tables
with app.app_context():
    db.create_all()

@app.route("/book_appointment", methods=["POST"])
def book_appointment():
    data = request.get_json()
    new_appointment = Appointment(
        patient_id=data["patient_id"],
        doctor_id=data["doctor_id"],
        date=data["date"],
        time=data["time"]
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({
        "message": "Appointment booked successfully!",
        "appointment": {
            "id": new_appointment.id,
            "patient_id": new_appointment.patient_id,
            "doctor_id": new_appointment.doctor_id,
            "date": new_appointment.date,
            "time": new_appointment.time,
            "status": new_appointment.status
        }
    }), 201

@app.route("/appointments", methods=["GET"])
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify({
        "appointments": [
            {
                "id": a.id,
                "patient_id": a.patient_id,
                "doctor_id": a.doctor_id,
                "date": a.date,
                "time": a.time,
                "status": a.status
            }
            for a in appointments
        ]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
