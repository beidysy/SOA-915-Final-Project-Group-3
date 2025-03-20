import os

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://doctor_admin:doctor_pass@localhost/doctor_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

