from sqlalchemy.orm import Session
from datetime import datetime

from . import models, schemas


# -------- Users --------

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        role=user.role,
        created_at=datetime.utcnow(),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


# -------- Patients --------

def create_patient(db: Session, patient: schemas.PatientCreate) -> models.Patient:
    db_patient = models.Patient(
        user_id=patient.user_id,
        age=patient.age,
        gender=patient.gender,
        blood_group=patient.blood_group,
        allergies=patient.allergies,
        medical_history=patient.medical_history,
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def get_patient(db: Session, patient_id: str):
    return db.query(models.Patient).filter(models.Patient.patient_id == patient_id).first()


def get_patient_by_user(db: Session, user_id: str):
    return db.query(models.Patient).filter(models.Patient.user_id == user_id).first()


# -------- Appointments --------

def create_appointment(db: Session, appointment: schemas.AppointmentCreate) -> models.Appointment:
    db_apt = models.Appointment(
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        department=appointment.department,
        scheduled_time=appointment.scheduled_time,
        status="Scheduled",
        created_at=datetime.utcnow(),
    )
    db.add(db_apt)
    db.commit()
    db.refresh(db_apt)
    return db_apt


def get_appointments_for_patient(db: Session, patient_id: str):
    return (
        db.query(models.Appointment)
        .filter(models.Appointment.patient_id == patient_id)
        .order_by(models.Appointment.scheduled_time.desc())
        .all()
    )


from .models import Vitals

def create_vitals(db: Session, data: schemas.VitalCreate):
    vital_id = str(uuid.UUID(bytes=uuid.uuid4().bytes))
    db_vital = Vitals(
        vital_id=vital_id,
        patient_id=data.patient_id,
        temperature=data.temperature,
        pulse=data.pulse,
        bp=data.bp,
        oxygen=data.oxygen,
        notes=data.notes,
        recorded_at=datetime.datetime.now()
    )
    db.add(db_vital)
    db.commit()
    db.refresh(db_vital)
    return db_vital


def get_patient_vitals(db: Session, patient_id: str):
    return db.query(Vitals).filter(Vitals.patient_id == patient_id).all()
