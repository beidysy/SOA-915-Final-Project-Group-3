from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure SQLite Database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "patients.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define Patient Model
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    new_patient = Patient(name=data["name"], age=data["age"], email=data["email"])
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({"message": "Patient registered successfully!", "patient": {"id": new_patient.id, "name": new_patient.name, "age": new_patient.age, "email": new_patient.email}}), 201

@app.route("/patients", methods=["GET"])
def get_patients():
    patients = Patient.query.all()
    return jsonify({"patients": [{"id": p.id, "name": p.name, "age": p.age, "email": p.email} for p in patients]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

