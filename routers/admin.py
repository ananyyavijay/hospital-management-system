from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func as sqlfunc, and_
from typing import Optional
import math

from database import get_db

from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment

from dependencies import require_role
from models.user import User

from schemas.admin import (
    PaginatedResponse,
    AdminPatientOut,
    AdminDoctorOut,
    AdminAppointmentOut,
    AdminStatsOut
)


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# ── GET ALL PATIENTS ──────────────────────────────────────────────────────────

@router.get(
    "/patients",
    response_model=PaginatedResponse[AdminPatientOut]
)
def admin_list_patients(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    blood_group: Optional[str] = None,
    active_only: bool = True,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_role("admin")
    )
):

    query = select(Patient)

    filters = []

    # Blood group filter
    if blood_group:
        filters.append(
            Patient.blood_group == blood_group
        )

    # Active filter
    if active_only:
        filters.append(
            Patient.is_active == True
        )

    if filters:
        query = query.where(
            and_(*filters)
        )

    # Total count
    total = len(
        db.scalars(query).all()
    )

    # Pagination
    patients = db.scalars(
        query.offset(
            (page - 1) * limit
        ).limit(limit)
    ).all()

    return PaginatedResponse(
        total=total,
        page=page,
        limit=limit,
        pages=math.ceil(total / limit)
        if total else 1,

        data=patients
    )


# ── GET ALL DOCTORS ───────────────────────────────────────────────────────────

@router.get(
    "/doctors",
    response_model=PaginatedResponse[AdminDoctorOut]
)
def admin_list_doctors(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    specialization: Optional[str] = None,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_role("admin")
    )
):

    query = select(Doctor)

    # Case-insensitive partial match
    if specialization:
        query = query.where(
            Doctor.specialization.ilike(
                f"%{specialization}%"
            )
        )

    total = len(
        db.scalars(query).all()
    )

    doctors = db.scalars(
        query.offset(
            (page - 1) * limit
        ).limit(limit)
    ).all()

    return PaginatedResponse(
        total=total,
        page=page,
        limit=limit,
        pages=math.ceil(total / limit)
        if total else 1,

        data=doctors
    )


# ── GET ALL APPOINTMENTS ──────────────────────────────────────────────────────

@router.get(
    "/appointments",
    response_model=PaginatedResponse[
        AdminAppointmentOut
    ]
)
def admin_list_appointments(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_role("admin")
    )
):

    query = select(Appointment)

    # Filter by status
    if status:
        query = query.where(
            Appointment.status == status
        )

    total = len(
        db.scalars(query).all()
    )

    appointments = db.scalars(
        query.offset(
            (page - 1) * limit
        ).limit(limit)
    ).all()

    return PaginatedResponse(
        total=total,
        page=page,
        limit=limit,
        pages=math.ceil(total / limit)
        if total else 1,

        data=appointments
    )


# ── ADMIN STATS ───────────────────────────────────────────────────────────────

@router.get(
    "/stats",
    response_model=AdminStatsOut
)
def admin_stats(
    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_role("admin")
    )
):

    total_patients = db.scalar(
        select(
            sqlfunc.count(Patient.id)
        )
    )

    active_patients = db.scalar(
        select(
            sqlfunc.count(Patient.id)
        ).where(
            Patient.is_active == True
        )
    )

    total_doctors = db.scalar(
        select(
            sqlfunc.count(Doctor.id)
        )
    )

    total_appointments = db.scalar(
        select(
            sqlfunc.count(Appointment.id)
        )
    )

    scheduled_count = db.scalar(
        select(
            sqlfunc.count(Appointment.id)
        ).where(
            Appointment.status == "Scheduled"
        )
    )

    completed_count = db.scalar(
        select(
            sqlfunc.count(Appointment.id)
        ).where(
            Appointment.status == "Completed"
        )
    )

    cancelled_count = db.scalar(
        select(
            sqlfunc.count(Appointment.id)
        ).where(
            Appointment.status == "Cancelled"
        )
    )

    return AdminStatsOut(
        total_patients=total_patients,

        active_patients=active_patients,

        total_doctors=total_doctors,

        total_appointments=total_appointments,

        by_status={
            "Scheduled": scheduled_count,
            "Completed": completed_count,
            "Cancelled": cancelled_count
        }
    )