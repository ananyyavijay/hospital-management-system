from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from database import get_db

from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from models.medical_record import MedicalRecord
from schemas.dashboard import PatientDashboardResponse, DashboardAppointment, DashboardPatientInfo, DashboardRecord, DashboardStats

router = APIRouter()

@router.get(
    "/{patient_id}/dashboard",
    response_model=PatientDashboardResponse
)
def get_dashboard(
    patient_id: str,
    db: Session = Depends(get_db)
    ):

    patient = db.scalar(
        select(Patient).where(
            Patient.patient_id == patient_id
        )
    )

    if not patient or not patient.is_active:
        raise HTTPException(
            status_code=404,
            detail="Patient not found or inactive"
        )

    appointments = db.scalars(
        select(Appointment).where(
            Appointment.patient_id == patient_id
        )
    ).all()

    upcoming_appointments = []
    past_appointments = []

    completed_count = 0

    for appt in appointments:

        doctor = db.scalar(
            select(Doctor).where(
                Doctor.doctor_id == appt.doctor_id
            )
        )

        doctor_name = (
            doctor.name if doctor else "Unknown Doctor"
        )

        appointment_data = DashboardAppointment(
            appointment_id=appt.appointment_id,
            doctor_name=doctor_name,
            time_slot=appt.time_slot,
            status=appt.status
        )

        if appt.status == "Scheduled":
            upcoming_appointments.append(
                appointment_data
            )

        elif appt.status in [
            "Completed",
            "Cancelled"
        ]:
            past_appointments.append(
                appointment_data
            )

        if appt.status == "Completed":
            completed_count += 1

    medical_records = db.scalars(
        select(MedicalRecord).where(
            MedicalRecord.patient_id == patient_id
        )
    ).all()

    stats = DashboardStats(
        total_appointments=len(appointments),
        completed_appointments=completed_count,
        upcoming_count=len(upcoming_appointments)
    )

    return PatientDashboardResponse(
        patient=DashboardPatientInfo.model_validate(
            patient
        ),

        upcoming_appointments=upcoming_appointments,

        past_appointments=past_appointments,

        medical_records=[
            DashboardRecord.model_validate(record)
            for record in medical_records
        ],

        stats=stats
    )