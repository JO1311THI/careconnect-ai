from fastapi import FastAPI

from .database import Base, engine
from . import models
from .routers import users, patients, appointments, vitals, admin, doctor, nurse, ai

# Create all tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CareConnect AI - Backend MVP",
    description="Basic backend with Users, Patients, and Appointments using FastAPI + MySQL",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"message": "CareConnect AI backend is running"}


# Include routers
app.include_router(users.router)
app.include_router(patients.router)
app.include_router(appointments.router)
app.include_router(vitals.router)
app.include_router(doctor.router)
app.include_router(nurse.router)
app.include_router(ai.router)
app.include_router(admin.router)

