from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure SQLite Database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "doctors.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define Doctor Model
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    availability = db.Column(db.String(200), nullable=False)  # Store as comma-separated values

# Create the database tables
with app.app_context():
    db.create_all()

@app.route("/add_doctor", methods=["POST"])
def add_doctor():
    data = request.get_json()
    new_doctor = Doctor(
        name=data["name"],
        specialty=data["specialty"],
        availability=",".join(data["availability"])  # Convert list to string
    )
    db.session.add(new_doctor)
    db.session.commit()
    return jsonify({
        "message": "Doctor added successfully!",
        "doctor": {
            "id": new_doctor.id,
            "name": new_doctor.name,
            "specialty": new_doctor.specialty,
            "availability": new_doctor.availability.split(",")  # Convert back to list
        }
    }), 201

@app.route("/doctors", methods=["GET"])
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify({
        "doctors": [
            {"id": d.id, "name": d.name, "specialty": d.specialty, "availability": d.availability.split(",")}
            for d in doctors
        ]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
