from datetime import datetime, date
from pydantic import BaseModel, EmailStr
from typing import Optional, List


# =========================================================
#                       USER
# =========================================================

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role: str  # Patient / Nurse / Doctor / Admin


class UserCreate(UserBase):
    pass


class UserOut(UserBase):
    user_id: str
    created_at: datetime
    last_login: Optional[datetime] = None

    model_config = {"from_attributes": True}


# =========================================================
#                       PATIENT
# =========================================================

class PatientBase(BaseModel):
    age: Optional[int] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None


class PatientCreate(PatientBase):
    user_id: str


class PatientOut(PatientBase):
    patient_id: str
    user: UserOut

    model_config = {"from_attributes": True}


# =========================================================
#                       DOCTOR
# =========================================================

class DoctorBase(BaseModel):
    specialization: str
    experience: Optional[int] = None


class DoctorCreate(DoctorBase):
    user_id: str


class DoctorOut(DoctorBase):
    doctor_id: str
    user: UserOut

    model_config = {"from_attributes": True}


# =========================================================
#                       NURSE
# =========================================================

class NurseBase(BaseModel):
    department: Optional[str] = None


class NurseCreate(NurseBase):
    user_id: str


class NurseOut(NurseBase):
    nurse_id: str
    user: UserOut

    model_config = {"from_attributes": True}


# =========================================================
#                       APPOINTMENT
# =========================================================

class AppointmentBase(BaseModel):
    patient_id: str
    doctor_id: str
    department: Optional[str] = None
    scheduled_time: datetime


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentOut(AppointmentBase):
    appointment_id: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class AppointmentList(BaseModel):
    items: List[AppointmentOut]


# =========================================================
#                       VITALS
# =========================================================

class VitalBase(BaseModel):
    patient_id: str
    temperature: str
    pulse: str
    bp: str
    oxygen: str
    notes: Optional[str] = None


class VitalCreate(VitalBase):
    pass


class VitalOut(VitalBase):
    vital_id: str
    recorded_at: datetime

    model_config = {"from_attributes": True}


# =========================================================
#                       DIAGNOSIS
# =========================================================

class DiagnosisBase(BaseModel):
    patient_id: str
    doctor_id: str
    appointment_id: Optional[str] = None
    summary: str
    details: Optional[str] = None


class DiagnosisCreate(DiagnosisBase):
    pass


class Diagnosis(BaseModel):
    id: str
    patient_id: str
    doctor_id: str
    appointment_id: Optional[str]
    summary: str
    details: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


# =========================================================
#                       PRESCRIPTION
# =========================================================

class PrescriptionBase(BaseModel):
    patient_id: str
    doctor_id: str
    medication_name: str
    dosage: Optional[str] = None
    instructions: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class PrescriptionCreate(PrescriptionBase):
    pass


class Prescription(BaseModel):
    id: str
    patient_id: str
    doctor_id: str
    medication_name: str
    dosage: Optional[str]
    instructions: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    created_at: datetime

    model_config = {"from_attributes": True}


# =========================================================
#                       ADMIN SUMMARY
# =========================================================

class AdminStats(BaseModel):
    total_users: int
    total_patients: int
    total_doctors: int
    total_nurses: int
    total_appointments: int
    total_vitals: int


# =========================================================
#                       AI CHAT
# =========================================================

class AIRequest(BaseModel):
    message: str


class AIResponse(BaseModel):
    reply: str
