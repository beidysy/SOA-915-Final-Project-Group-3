import os

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://root:root@postgres/notification_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

