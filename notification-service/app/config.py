import os

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://notification_admin:notification_pass@localhost/notification_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

