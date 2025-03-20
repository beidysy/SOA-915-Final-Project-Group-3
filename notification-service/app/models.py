from app.database import db

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default="Pending")  # Pending, Sent, Failed
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

