# tests/e2e/test_full_system_flow.py

import time
import random
import requests

BASE_URL = "http://192.168.49.2"
PATIENT_PORT = "30001"
DOCTOR_PORT = "30002"
APPOINTMENT_PORT = "30003"
NOTIFICATION_PORT = "30004"

def test_end_to_end_flow():
    timestamp = int(time.time())
    patient_email = f"e2e+{timestamp}@example.com"
    patient_phone = f"555{random.randint(1000000, 9999999)}"

    # 1. Register patient
    patient_payload = {
        "name": "E2E Test Patient",
        "age": 32,
        "email": patient_email,
        "phone": patient_phone
    }
    res = requests.post(f"{BASE_URL}:{PATIENT_PORT}/patients", json=patient_payload)
    assert res.status_code == 201, f"Patient creation failed: {res.text}"

    # 2. Get patient ID
    res = requests.get(f"{BASE_URL}:{PATIENT_PORT}/patients")
    patient_id = next((p["id"] for p in res.json() if p["email"] == patient_email), None)
    assert patient_id, f"Could not retrieve patient ID for {patient_email}"

    # 3. Register doctor
    doctor_email = f"e2e.doctor+{timestamp}@example.com"
    doctor_phone = f"666{random.randint(1000000, 9999999)}"
    doctor_payload = {
        "name": "E2E Dr.",
        "specialty": "General",
        "email": doctor_email,
        "phone": doctor_phone
    }
    res = requests.post(f"{BASE_URL}:{DOCTOR_PORT}/doctors", json=doctor_payload)
    assert res.status_code == 201, f"Doctor creation failed: {res.text}"

    # 4. Get doctor ID
    res = requests.get(f"{BASE_URL}:{DOCTOR_PORT}/doctors")
    doctor_id = next((d["id"] for d in res.json() if d["email"] == doctor_email), None)
    assert doctor_id, f"Could not retrieve doctor ID for {doctor_email}"

    # 5. Book appointment
    appointment_payload = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "date": "2025-06-15",
        "time": "10:00",
        "status": "Scheduled"
    }
    res = requests.post(
        f"{BASE_URL}:{APPOINTMENT_PORT}/appointments",
        headers={"X-Patient-ID": str(patient_id)},
        json=appointment_payload
    )
    assert res.status_code == 201, f"Appointment creation failed: {res.text}"

    # 6. Get appointments and verify creation
    res = requests.get(f"{BASE_URL}:{APPOINTMENT_PORT}/appointments")
    assert res.status_code == 200, "Failed to fetch appointments"
    appointments = res.json()
    matching_appointments = [
        a for a in appointments
        if a["patient_id"] == patient_id and a["doctor_id"] == doctor_id
    ]
    assert matching_appointments, "Appointment not found in the system"

    # 7. Verify notification was created
    res = requests.get(
        f"{BASE_URL}:{NOTIFICATION_PORT}/notifications",
        headers={"X-Patient-ID": str(patient_id)}
    )
    assert res.status_code == 200, f"Failed to fetch notifications: {res.text}"
    notifications = res.json()

    print("📬 Notifications received:", notifications)  # 👈 DEBUG
    assert notifications, "No notifications returned"

