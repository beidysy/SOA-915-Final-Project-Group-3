import os

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://appointment_admin:appointment_pass@localhost/appointment_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

