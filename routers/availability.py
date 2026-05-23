from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Dict
import re

from database import get_db
from models.doctor import Doctor


router = APIRouter(
    prefix="/doctors",
    tags=["Availability"]
)

class SetAvailabilityRequest(BaseModel):
    date: str
    slots: List[str]

    @field_validator("date")
    @classmethod
    def validate_date(cls, value: str):

        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise ValueError(
                "Date must be in YYYY-MM-DD format"
            )

        return value

    @field_validator("slots")
    @classmethod
    def validate_slots(cls, value: List[str]):

        pattern = r"^([01]\d|2[0-3]):([0-5]\d)$"

        for slot in value:

            if not re.fullmatch(pattern, slot):
                raise ValueError(
                    f"Invalid slot format: {slot}"
                )

        return value


class AvailabilityResponse(BaseModel):
    doctor_id: str
    availability: Dict[str, List[str]]


@router.post("/{doctor_id}/availability")
def set_availability(
    doctor_id: str,
    data: SetAvailabilityRequest,
    db: Session = Depends(get_db)
):

    doctor = db.scalar(
        select(Doctor).where(
            Doctor.doctor_id == doctor_id
        )
    )

    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )

    if doctor.availability is None:
        doctor.availability = {}

    doctor.availability[data.date] = data.slots

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return {
        "message": "Availability updated",
        "doctor_id": doctor.doctor_id,
        "availability": doctor.availability
    }


@router.get(
    "/{doctor_id}/availability",
    response_model=AvailabilityResponse
)
def get_availability(
    doctor_id: str,
    db: Session = Depends(get_db)
):

    doctor = db.scalar(
        select(Doctor).where(
            Doctor.doctor_id == doctor_id
        )
    )

    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )

    return {
        "doctor_id": doctor.doctor_id,
        "availability": doctor.availability or {}
    }


@router.get("/{doctor_id}/availability/{date}")
def get_availability_for_date(
    doctor_id: str,
    date: str,
    db: Session = Depends(get_db)
):

    # Validate date format
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Date must be YYYY-MM-DD"
        )

    doctor = db.scalar(
        select(Doctor).where(
            Doctor.doctor_id == doctor_id
        )
    )

    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )

    availability = doctor.availability or {}

    if date not in availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No availability for this date"
        )

    return {
        "doctor_id": doctor.doctor_id,
        "date": date,
        "slots": availability[date]
    }