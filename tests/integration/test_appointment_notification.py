import requests
import time
import random

BASE_URL = "http://192.168.49.2"

PATIENT_PORT = "30001"
DOCTOR_PORT = "30002"
APPOINTMENT_PORT = "30003"
NOTIFICATION_PORT = "30004"

def test_full_appointment_flow():
    timestamp = int(time.time())
    unique_email = f"integration+{timestamp}@example.com"
    unique_phone = f"555{random.randint(1000000, 9999999)}"

    # 1. Create a new patient
    patient_payload = {
        "name": "Integration Test Patient",
        "age": 28,
        "email": unique_email,
        "phone": unique_phone
    }
    patient_response = requests.post(f"{BASE_URL}:{PATIENT_PORT}/patients", json=patient_payload)
    print("✅ Patient response:", patient_response.status_code, patient_response.text)
    assert patient_response.status_code == 201, f"Patient creation failed: {patient_response.text}"

    # 2. Fetch patient ID by searching all patients
    all_patients_response = requests.get(f"{BASE_URL}:{PATIENT_PORT}/patients")
    assert all_patients_response.status_code == 200, "Failed to fetch patients list"
    patients = all_patients_response.json()
    patient_id = next((p["id"] for p in patients if p["email"] == unique_email), None)
    assert patient_id, f"No matching patient found for email: {unique_email}"

    # 3. Create a new doctor
    unique_doc_email = f"dr.integration+{timestamp}@example.com"
    unique_doc_phone = f"666{random.randint(1000000, 9999999)}"
    doctor_payload = {
        "name": "Integration Dr.",
        "specialty": "Testing",
        "email": unique_doc_email,
        "phone": unique_doc_phone
    }
    doctor_response = requests.post(f"{BASE_URL}:{DOCTOR_PORT}/doctors", json=doctor_payload)
    print("✅ Doctor response:", doctor_response.status_code, doctor_response.text)
    assert doctor_response.status_code == 201, f"Doctor creation failed: {doctor_response.text}"

    # Fetch doctor ID by email
    all_doctors_response = requests.get(f"{BASE_URL}:{DOCTOR_PORT}/doctors")
    assert all_doctors_response.status_code == 200, "Failed to fetch doctors list"
    doctors = all_doctors_response.json()
    doctor_id = next((d["id"] for d in doctors if d["email"] == unique_doc_email), None)
    assert doctor_id, f"No matching doctor found for email: {unique_doc_email}"

    # 4. Create an appointment
    appointment_payload = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "date": "2025-06-01",
        "time": "11:00",
        "status": "Scheduled"
    }
    appointment_response = requests.post(
        f"{BASE_URL}:{APPOINTMENT_PORT}/appointments",
        headers={"X-Patient-ID": str(patient_id)},
        json=appointment_payload
    )
    print("✅ Appointment response:", appointment_response.status_code, appointment_response.text)
    assert appointment_response.status_code == 201, f"Appointment creation failed: {appointment_response.text}"

    # 5. Get appointment ID (by filtering appointments)
    all_appointments_response = requests.get(f"{BASE_URL}:{APPOINTMENT_PORT}/appointments")
    assert all_appointments_response.status_code == 200, "Failed to fetch appointments list"
    appointments = all_appointments_response.json()
    appointment_id = next(
        (
            a["id"] for a in appointments
            if a["patient_id"] == patient_id and a["doctor_id"] == doctor_id and a["date"] == "2025-06-01"
        ),
        None
    )
    assert appointment_id, "No appointment ID found after creation"

    # 6. Send a notification
    notification_payload = {
        "appointment_id": appointment_id,
        "message": "This is an integration test notification."
    }
    notification_response = requests.post(
        f"{BASE_URL}:{NOTIFICATION_PORT}/notifications",
        headers={"X-Patient-ID": str(patient_id)},
        json=notification_payload
    )
    print("✅ Notification response:", notification_response.status_code, notification_response.text)
    assert notification_response.status_code == 201, f"Notification failed: {notification_response.text}"
    assert "Notification sent successfully" in notification_response.json()["message"]

