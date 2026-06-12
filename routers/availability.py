from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Dict
from datetime import datetime
import re

from database import get_db
from models.doctor import Doctor


router = APIRouter(
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

    # Existing availability
    availability = dict(doctor.availability or {})

    # Create date key if not present
    if data.date not in availability:
        availability[data.date] = []

    # Existing slots
    existing_slots = set()

    # Convert old slots back to 24-hour for sorting consistency
    for slot in availability[data.date]:

        try:
            old_time = datetime.strptime(
                slot,
                "%I:%M %p"
            ).strftime("%H:%M")

            existing_slots.add(old_time)

        except:
            existing_slots.add(slot)

    # Add new slots
    for slot in data.slots:
        existing_slots.add(slot)

    # Sort chronologically
    sorted_slots = sorted(
        existing_slots,
        key=lambda x: datetime.strptime(x, "%H:%M")
    )

    # Convert to AM/PM
    formatted_slots = [
        datetime.strptime(
            slot,
            "%H:%M"
        ).strftime("%I:%M %p")
        for slot in sorted_slots
    ]

    availability[data.date] = formatted_slots

    doctor.availability = availability

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

class RemoveAvailabilityRequest(BaseModel):
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


@router.delete("/{doctor_id}/availability")
def remove_availability(
    doctor_id: str,
    data: RemoveAvailabilityRequest,
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

    availability = dict(doctor.availability or {})

    if data.date not in availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No availability found for this date"
        )

    # Convert existing AM/PM slots back to 24-hour format
    existing_slots = []

    for slot in availability[data.date]:

        try:
            converted = datetime.strptime(
                slot,
                "%I:%M %p"
            ).strftime("%H:%M")

            existing_slots.append(converted)

        except:
            existing_slots.append(slot)

    # Remove requested slots
    updated_slots = [
        slot for slot in existing_slots
        if slot not in data.slots
    ]

    # Sort remaining slots
    updated_slots = sorted(
        updated_slots,
        key=lambda x: datetime.strptime(x, "%H:%M")
    )

    # Convert back to AM/PM
    formatted_slots = [
        datetime.strptime(
            slot,
            "%H:%M"
        ).strftime("%I:%M %p")
        for slot in updated_slots
    ]

    # If no slots left, remove date completely
    if not formatted_slots:
        del availability[data.date]

    else:
        availability[data.date] = formatted_slots

    doctor.availability = availability

    db.commit()
    db.refresh(doctor)

    return {
        "message": "Availability removed successfully",
        "doctor_id": doctor.doctor_id,
        "availability": doctor.availability
    }