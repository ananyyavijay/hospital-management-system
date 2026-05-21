from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from database import get_db
from models.doctor import Doctor
from schemas.doctor import DoctorCreate, DoctorResponse

router = APIRouter()

def generate_doctor_id(db: Session):

    count = db.scalar(
        select(func.count()).select_from(Doctor)
    ) + 1

    return f"D{count:03d}"

@router.post("", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
def create_doctors(
    doctor: DoctorCreate,
    db: Session = Depends(get_db)
):
    doctor_id = generate_doctor_id(db)
    
    new_doctor = Doctor(
        doctor_id=doctor_id,
        name=doctor.name,
        specialization=doctor.specialization,
        experience=doctor.experience,
        contact=doctor.contact,
        is_active=True
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor

@router.get("", response_model=list[DoctorResponse])
def list_doctors(
    specialization: str | None = None,
    db: Session = Depends(get_db)
):

    query = select(Doctor).where(
        Doctor.is_active == True
    )
    if specialization:
        query = query.where(
            Doctor.specialization == specialization
        )

    doctors = db.execute(query).scalars().all()

    return doctors


@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: str,
    db: Session = Depends(get_db)):

    query = select(Doctor).where(
        Doctor.doctor_id == doctor_id,
        Doctor.is_active == True
    )
    doctor = db.execute(query).scalar_one_or_none()

    if doctor is None:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )
    return doctor

@router.delete(
    "/{doctor_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_doctor(
    doctor_id: str,
    db: Session = Depends(get_db)
):

    query = select(Doctor).where(
        Doctor.doctor_id == doctor_id,
        Doctor.is_active == True
    )

    doctor = db.execute(query).scalar_one_or_none()

    if doctor is None:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    doctor.is_active = False

    db.commit()

    return