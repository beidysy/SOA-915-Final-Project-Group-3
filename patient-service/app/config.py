import os

class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@postgres/patient_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 👇 Add this line inside the class to print
    print("🧠 Using DB URI:", SQLALCHEMY_DATABASE_URI)

