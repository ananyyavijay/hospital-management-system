from services.hospital_service import Hospital

from exceptions.hms_exceptions import (
    PatientNotFoundError,
    DoctorNotFoundError,
    SlotNotAvailableError,
    AppointmentNotFoundError
)
import asyncio
from fastapi import FastAPI
from db.connection import get_connection
from routers import patients, doctors, appointments, auth, availability, dashboard, records, admin
import os
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from models.medical_record import MedicalRecord
from models.user import User
from fastapi.middleware.cors import CORSMiddleware

# Updated 10 Jun to main.py

app = FastAPI(
    title="Hospital Management System",
    version="2.0.0",
    description="HMS v2 — FastAPI + PostgreSQL + Azure"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check — does NOT touch the database.
    Returns 200 when the app process is running.
    """
    return {
        "status": "ok",
        "service": "HMS API",
        "version": "2.0.0",
        "environment": os.getenv("APP_ENV", "unknown")
    }

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"]

)

app.include_router(
    patients.router,
    prefix="/patients",
    tags=["Patients"]
)

app.include_router(
    doctors.router,
    prefix="/doctors",
    tags=["Doctors"]
)

app.include_router(
    appointments.router,
    prefix="/appointments",
    tags=["Appointments"]
)
app.include_router(
    availability.router,
    prefix="/doctors",
    tags=["Availability"]
)

app.include_router(
    dashboard.router,
    prefix="/patients",
    tags=["Dashboard"]
)

app.include_router(
    records.router,
    prefix="/patients",
    tags=["Medical Records"]
)

app.include_router(
    admin.router,
    prefix="/admin",
    tags=["Admin"]
)

@app.get("/")
def home():
    return {"message": "Hospital API Running"}



async def main():


    hospital = Hospital()
    print('ALL OK')


    # # DOCTORS #

    # doc1 = Doctor(
    # doctor_id="D002",
    # name="Dr. Rina",
    # specialization="Gynecologist",
    # is_active=True
    # )

    # doc2 = Doctor(
    #     doctor_id="D003",
    #     name="Dr. Bedi",
    #     specialization="Surgeon",
    #     is_active=True
    # )


    # doc1.add_slot("10:15")
    # doc1.add_slot("11:15")

    # doc2.add_slot("11:30")


    # # PATIENTS #

    # pat1 = Patient(
    # patient_id="P012",
    # name="Richa",
    # blood_group="A+",
    # age=22,
    # contact="9876543211",
    # is_active=True
    # )

    # pat2 = Patient(
    #     patient_id="P015",
    #     name="Raja Bajaj",
    #     blood_group="AB+",
    #     age=32,
    #     contact="9876543212",
    #     is_active=True
    # )

    # pat3 = Patient(
    #     patient_id="P032",
    #     name="Ahana",
    #     blood_group="O+",
    #     age=29,
    #     contact="9876543213",
    #     is_active=True
    # )

    # # MEDICAL RECORDS  #

    # pat1.add_record("PCOD")

    # pat2.add_record("Bone Fracture")

    # pat1.add_record("Fever")

    # pat3.add_record("Sinus")

    # # REGISTER #

    # hospital.register_doctor(doc1)
    # hospital.register_doctor(doc2)

    # hospital.register_patient(pat1)
    # hospital.register_patient(pat2)
    # hospital.register_patient(pat3)


    # # BOOK APPOINTMENTS 
    # apt1 = await hospital.book_appointment(
    #     "P012",
    #     "D002",
    #     "10:15"
    # )

    # apt2 = await hospital.book_appointment(
    #     "P015",
    #     "D003",
    #     "11:30"
    # )

    # apt3 = await hospital.book_appointment(
    #     "P032",
    #     "D002",
    #     "11:15"
    # )


    # #  SLOT ERROR TEST #

    # try:

    #     await hospital.book_appointment(
    #         "P032",
    #         "D002",
    #         "10:15"
    #     )

    # except SlotNotAvailableError as s:

    #     print(s)


    # # INVALID PATIENT TEST #

    # try:

    #     await hospital.book_appointment(
    #         "P999",
    #         "D002",
    #         "10:15"
    #     )

    # except PatientNotFoundError as p:

    #     print(p)


    # # CANCEL APPOINTMENT #

    # hospital.cancel_appointment(
    #     apt3.appointment_id
    # )

    # print(doc1.available_slots)


    # # HOSPITAL SUMMARY #

    # print(hospital)


    # # SORTED PATIENTS  #

    # print("\nSORTED PATIENTS:\n")


    # patients = hospital.get_all_patients(True)

    # for patient in patients:

    #     print(patient)

    #     print("-" * 40)


    # # DOCTOR APPOINTMENTS #

    # print("\nDOCTOR APPOINTMENTS:\n")


    # appointments = hospital.get_doctor_appointments("D002")

    # for appointment in appointments:

    #     print(appointment)

    #     print("-" * 40)


    # # PATIENT REPORT #

    # print("\nPATIENT REPORT:\n")


    # for record in hospital.patient_report("P012"):

    #     print(record)


    # # ADMIN REPORT #

    # print("\nADMIN REPORT:\n")
    # hospital.admin_report()
    # await asyncio.sleep(1)

if __name__ == "__main__":

    asyncio.run(main())