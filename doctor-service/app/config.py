import os

class Config:
    #SQLALCHEMY_DATABASE_URI = "postgresql://root:root@postgres/doctor_db"
    #SQLALCHEMY_DATABASE_URI = "postgresql://group3:group3pass@postgres:5432/doctor_db"
    SQLALCHEMY_DATABASE_URI = "postgresql://group3:group3pass@localhost:5432/doctor_db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

