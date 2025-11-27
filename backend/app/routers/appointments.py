from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from ..database import get_db

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)


@router.post("/", response_model=schemas.AppointmentOut)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    # later we can add validation: patient exists, doctor exists, etc.
    return crud.create_appointment(db, appointment)


@router.get("/patient/{patient_id}", response_model=List[schemas.AppointmentOut])
def get_appointments_for_patient(patient_id: str, db: Session = Depends(get_db)):
    return crud.get_appointments_for_patient(db, patient_id)
