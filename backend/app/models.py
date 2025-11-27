from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime, date
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Text,
    DateTime,
    Date,
    ForeignKey,
)

from .database import Base


def generate_uuid() -> str:
    return str(uuid4())


class User(Base):
    __tablename__ = "users"

    user_id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    phone = Column(String(15), nullable=True)
    role = Column(String(50), nullable=False)  # Patient / Nurse / Doctor / Admin
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # Relationships
    patient_profile = relationship("Patient", back_populates="user", uselist=False)
    doctor_appointments = relationship(
        "Appointment",
        back_populates="doctor",
        foreign_keys="Appointment.doctor_id",
    )


class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    user_id = Column(String(36), ForeignKey("users.user_id"), nullable=False, unique=True)
    age = Column(Integer, nullable=True)
    gender = Column(String(10), nullable=True)
    blood_group = Column(String(5), nullable=True)
    allergies = Column(String(255), nullable=True)
    medical_history = Column(String(1000), nullable=True)

    user = relationship("User", back_populates="patient_profile")
    appointments = relationship("Appointment", back_populates="patient")


class Appointment(Base):
    __tablename__ = "appointments"

    appointment_id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    patient_id = Column(String(36), ForeignKey("patients.patient_id"), nullable=False)
    doctor_id = Column(String(36), ForeignKey("users.user_id"), nullable=False)
    department = Column(String(50), nullable=True)
    scheduled_time = Column(DateTime, nullable=False)
    status = Column(String(50), default="Scheduled")  # Scheduled / Completed / Cancelled
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("User", back_populates="doctor_appointments")

class Vitals(Base):
    __tablename__ = "vitals"

    vital_id = Column(String(36), primary_key=True, index=True)
    patient_id = Column(String(36), ForeignKey("patients.patient_id"))
    
    temperature = Column(String(10))
    pulse = Column(String(10))
    bp = Column(String(10))
    oxygen = Column(String(10))
    notes = Column(String(500))

    recorded_at = Column(DateTime)


# ---------- NEW: Diagnosis model ----------
class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id = Column(String(36), primary_key=True, index=True)
    patient_id = Column(String(36), ForeignKey("patients.patient_id"), nullable=False)
    doctor_id = Column(String(36), ForeignKey("users.user_id"), nullable=False)
    appointment_id = Column(String(36), ForeignKey("appointments.appointment_id"), nullable=True)

    summary = Column(String(255), nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# ---------- NEW: Prescription model ----------
class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(String(36), primary_key=True, index=True)
    patient_id = Column(String(36), ForeignKey("patients.patient_id"), nullable=False)
    doctor_id = Column(String(36), ForeignKey("users.user_id"), nullable=False)

    medication_name = Column(String(100), nullable=False)
    dosage = Column(String(100), nullable=True)
    instructions = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
