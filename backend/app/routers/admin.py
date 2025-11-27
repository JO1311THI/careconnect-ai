from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/admin", tags=["Admin"])


# -------- Stats -----------
@router.get("/stats")
def admin_stats(db: Session = Depends(get_db)):
    return {
        "total_users": db.query(models.User).count(),
        "total_patients": db.query(models.Patient).count(),
        "total_appointments": db.query(models.Appointment).count(),
        "total_vitals": db.query(models.Vitals).count(),
    }


# -------- Users -------------
@router.get("/users", response_model=List[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


# -------- Appointments -------------
@router.get("/appointments", response_model=List[schemas.AppointmentOut])
def get_all_appointments(db: Session = Depends(get_db)):
    return db.query(models.Appointment).all()


# -------- Vitals -------------
@router.get("/vitals", response_model=List[schemas.VitalOut])
def get_all_vitals(db: Session = Depends(get_db)):
    return db.query(models.Vitals).all()
