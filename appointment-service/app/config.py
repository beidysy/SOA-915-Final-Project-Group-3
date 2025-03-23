import os

class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@postgres/appointment_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

