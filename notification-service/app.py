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

    # Ensure appointment exists
    appointment_exists = any(a["id"] == data["appointment_id"] for a in appointment_data["appointments"])
    if not appointment_exists:
        return jsonify({"error": "Invalid appointment_id"}), 400

    new_notification = Notification(
        appointment_id=data["appointment_id"],
        message=f"Reminder: You have an appointment on {data['date']} at {data['time']}"
    )
    db.session.add(new_notification)
    db.session.commit()
    return jsonify({
        "message": "Notification sent successfully!",
        "notification": {
            "id": new_notification.id,
            "appointment_id": new_notification.appointment_id,
            "message": new_notification.message,
            "status": new_notification.status
        }
    }), 201

@app.route("/notifications", methods=["GET"])
def get_notifications():
    notifications = Notification.query.all()
    return jsonify({
        "notifications": [
            {"id": n.id, "appointment_id": n.appointment_id, "message": n.message, "status": n.status}
            for n in notifications
        ]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)

