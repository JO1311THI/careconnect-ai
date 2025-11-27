from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/nurse", tags=["Nurse"])


@router.get("/today-appointments", response_model=List[schemas.AppointmentOut])
def get_todays_appointments(db: Session = Depends(get_db)):
    today = date.today()
    return (
        db.query(models.Appointment)
        .filter(models.Appointment.scheduled_time >= today)
        .filter(models.Appointment.scheduled_time < today.replace(day=today.day + 1))
        .all()
    )


@router.post("/vitals", response_model=schemas.VitalOut)
def record_vitals(data: schemas.VitalCreate, db: Session = Depends(get_db)):
    vitals = models.Vitals(
        vital_id=str(uuid4()),
        patient_id=data.patient_id,
        temperature=data.temperature,
        pulse=data.pulse,
        bp=data.bp,
        oxygen=data.oxygen,
        notes=data.notes,
        recorded_at=datetime.utcnow(),
    )
    db.add(vitals)
    db.commit()
    db.refresh(vitals)
    return vitals
