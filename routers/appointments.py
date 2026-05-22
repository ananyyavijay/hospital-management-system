from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from database import get_db
from models.appointment import Appointment
from models.patient import Patient
from models.doctor import Doctor
from schemas.appointment import (
    AppointmentCreate,
    AppointmentResponse
)

router = APIRouter()


# Generate Appointment ID
def generate_appointment_id(db: Session):

    count = db.scalar(
        select(func.count()).select_from(Appointment)
    ) + 1

    return f"A{count:03d}"

# Create Appointment
@router.post(
    "",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db)
):

    # Check Patient
    patient_query = select(Patient).where(
        Patient.patient_id == appointment.patient_id,
        Patient.is_active == True
    )

    patient = db.execute(patient_query).scalar_one_or_none()

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # Check Doctor
    doctor_query = select(Doctor).where(
        Doctor.doctor_id == appointment.doctor_id,
        Doctor.is_active == True
    )

    doctor = db.execute(doctor_query).scalar_one_or_none()

    if doctor is None:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    # Generate Appointment ID
    appointment_id = generate_appointment_id(db)

    # Create Appointment Object
    new_appointment = Appointment(
        appointment_id=appointment_id,
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        time_slot=appointment.time_slot,
        status=appointment.status
    )

    db.add(new_appointment)

    db.commit()
    db.refresh(new_appointment)

    return AppointmentResponse(
        appointment_id=new_appointment.appointment_id,
        patient_id=new_appointment.patient_id,
        doctor_id=new_appointment.doctor_id,
        time_slot=new_appointment.time_slot,
        status=new_appointment.status,
        created_at=new_appointment.created_at,
        patient_name=patient.name,
        doctor_name=doctor.name
    )


# List All Appointments
@router.get(
    "",
    response_model=list[AppointmentResponse]
)
def list_appointments(
    db: Session = Depends(get_db)
):

    query = select(Appointment)

    appointments = db.execute(query).scalars().all()

    response = []

    for appointment in appointments:

        response.append(
            AppointmentResponse(
                appointment_id=appointment.appointment_id,
                patient_id=appointment.patient_id,
                doctor_id=appointment.doctor_id,
                time_slot=appointment.time_slot,
                status=appointment.status,
                created_at=appointment.created_at,
                patient_name=appointment.patient.name,
                doctor_name=appointment.doctor.name
            )
        )

    return response


# Get Single Appointment
@router.get(
    "/{appointment_id}",
    response_model=AppointmentResponse
)
def get_appointment(
    appointment_id: str,
    db: Session = Depends(get_db)
):

    query = select(Appointment).where(
        Appointment.appointment_id == appointment_id
    )

    appointment = db.execute(query).scalar_one_or_none()

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    return AppointmentResponse(
        appointment_id=appointment.appointment_id,
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        time_slot=appointment.time_slot,
        status=appointment.status,
        created_at=appointment.created_at,
        patient_name=appointment.patient.name,
        doctor_name=appointment.doctor.name
    )


# Cancel Appointment
@router.put(
    "/{appointment_id}/cancel",
    response_model=AppointmentResponse
)
def cancel_appointment(
    appointment_id: str,
    db: Session = Depends(get_db)
):

    query = select(Appointment).where(
        Appointment.appointment_id == appointment_id
    )

    appointment = db.execute(query).scalar_one_or_none()

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    if appointment.status == "Cancelled":
        raise HTTPException(
            status_code=400,
            detail="Appointment already cancelled"
        )

    appointment.status = "Cancelled"

    db.commit()
    db.refresh(appointment)

    return AppointmentResponse(
        appointment_id=appointment.appointment_id,
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        time_slot=appointment.time_slot,
        status=appointment.status,
        created_at=appointment.created_at,
        patient_name=appointment.patient.name,
        doctor_name=appointment.doctor.name
    )