from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/doctor", tags=["Doctor"])


@router.get("/{doctor_id}/appointments", response_model=List[schemas.AppointmentOut])
def get_doctor_appointments(doctor_id: str, db: Session = Depends(get_db)):
    return db.query(models.Appointment).filter(models.Appointment.doctor_id == doctor_id).all()


@router.post("/diagnosis/", response_model=schemas.Diagnosis)
def create_diagnosis(data: schemas.DiagnosisCreate, db: Session = Depends(get_db)):
    diag = models.Diagnosis(
        id=str(uuid4()),
        patient_id=data.patient_id,
        doctor_id=data.doctor_id,
        appointment_id=data.appointment_id,
        summary=data.summary,
        details=data.details,
    )
    db.add(diag)
    db.commit()
    db.refresh(diag)
    return diag


@router.post("/prescription/", response_model=schemas.Prescription)
def create_prescription(data: schemas.PrescriptionCreate, db: Session = Depends(get_db)):
    pres = models.Prescription(
        id=str(uuid4()),
        patient_id=data.patient_id,
        doctor_id=data.doctor_id,
        medication_name=data.medication_name,
        dosage=data.dosage,
        instructions=data.instructions,
        start_date=data.start_date,
        end_date=data.end_date,
    )
    db.add(pres)
    db.commit()
    db.refresh(pres)
    return pres
