import requests

BASE_URL = "http://127.0.0.1:8000"  # FastAPI backend


# ---------- User / Patient / Appointment ----------

def create_user(data):
    return requests.post(f"{BASE_URL}/users/", json=data)


def create_patient(data):
    return requests.post(f"{BASE_URL}/patients/", json=data)


def create_appointment(data):
    return requests.post(f"{BASE_URL}/appointments/", json=data)


def get_patient_appointments(patient_id: str):
    return requests.get(f"{BASE_URL}/appointments/patient/{patient_id}")


# ---------- Vitals ----------

def add_vitals(payload):
    return requests.post(f"{BASE_URL}/vitals/", json=payload)


def get_vitals(patient_id: str):
    return requests.get(f"{BASE_URL}/vitals/{patient_id}")


# ---------- Admin ----------

def get_admin_stats():
    return requests.get(f"{BASE_URL}/admin/stats")


def get_all_users():
    return requests.get(f"{BASE_URL}/admin/users")


def get_all_appointments():
    return requests.get(f"{BASE_URL}/admin/appointments")


def get_all_vitals():
    return requests.get(f"{BASE_URL}/admin/vitals")


# ---------- Doctor ----------

def get_doctor_appointments(doctor_id: str):
    return requests.get(f"{BASE_URL}/doctor/{doctor_id}/appointments")


def get_doctor_patients(doctor_id: str):
    return requests.get(f"{BASE_URL}/doctor/{doctor_id}/patients")


def create_diagnosis(payload):
    return requests.post(f"{BASE_URL}/doctor/diagnosis", json=payload)


def get_doctor_diagnoses(doctor_id: str):
    return requests.get(f"{BASE_URL}/doctor/{doctor_id}/diagnoses")


def create_prescription(payload):
    return requests.post(f"{BASE_URL}/doctor/prescriptions", json=payload)


def get_doctor_prescriptions(doctor_id: str):
    return requests.get(f"{BASE_URL}/doctor/{doctor_id}/prescriptions")


# ---------- Nurse ----------

def get_today_appointments_for_nurse():
    return requests.get(f"{BASE_URL}/nurse/today-appointments")


# ---------- AI & Chat Intake ----------

def ai_diagnosis(payload):
    return requests.post(f"{BASE_URL}/ai/diagnosis-assistant", json=payload)


def intake_chat(message: str):
    return requests.post(f"{BASE_URL}/ai/intake-chat", json={"message": message})
