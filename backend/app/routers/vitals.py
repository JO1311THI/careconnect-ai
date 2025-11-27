from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud

router = APIRouter(prefix="/vitals", tags=["Vitals"])


@router.post("/")
def add_vitals(data: schemas.VitalCreate, db: Session = Depends(get_db)):
    return crud.create_vitals(db, data)


@router.get("/{patient_id}")
def get_vitals(patient_id: str, db: Session = Depends(get_db)):
    return crud.get_patient_vitals(db, patient_id)
