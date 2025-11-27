from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, crud
from ..database import get_db

router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)


@router.post("/", response_model=schemas.PatientOut)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    user = crud.get_user(db, patient.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing = crud.get_patient_by_user(db, patient.user_id)
    if existing:
        raise HTTPException(status_code=400, detail="Patient profile already exists")

    return crud.create_patient(db, patient)


@router.get("/{patient_id}", response_model=schemas.PatientOut)
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    db_patient = crud.get_patient(db, patient_id)
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient
