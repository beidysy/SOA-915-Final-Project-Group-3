import os

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://patient_admin:patient_pass@localhost/patient_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

