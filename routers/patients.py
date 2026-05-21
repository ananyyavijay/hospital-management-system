from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from database import get_db
from models.patient import Patient
from schemas.patient import PatientCreate, PatientResponse

router = APIRouter()


# Helper function for auto ID generation
def generate_patient_id(db: Session):

    count = db.query(Patient).count() + 1

    return f"P{count:03d}"


# CREATE PATIENT
@router.post(
    "",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED
)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db)
):

    patient_id = generate_patient_id(db)

    new_patient = Patient(
        patient_id=patient_id,
        name=patient.name,
        blood_group=patient.blood_group,
        age=patient.age,
        contact=patient.contact,
        is_active=True
    )

    db.add(new_patient)

    db.commit()

    db.refresh(new_patient)

    return new_patient


# GET ALL PATIENTS
@router.get(
    "",
    response_model=list[PatientResponse]
)
def list_patients(
    blood_group: str | None = None,
    db: Session = Depends(get_db)
):

    query = select(Patient).where(
        Patient.is_active == True
    )

    if blood_group:
        query = query.where(
            Patient.blood_group == blood_group
        )

    patients = db.execute(query).scalars().all()

    return patients


# GET PATIENT BY ID
@router.get(
    "/{patient_id}",
    response_model=PatientResponse
)
def get_patient(
    patient_id: str,
    db: Session = Depends(get_db)
):

    query = select(Patient).where(
        Patient.patient_id == patient_id
    )

    patient = db.execute(query).scalar_one_or_none()

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient


# SOFT DELETE
@router.delete(
    "/{patient_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_patient(
    patient_id: str,
    db: Session = Depends(get_db)
):

    query = select(Patient).where(
        Patient.patient_id == patient_id
    )

    patient = db.execute(query).scalar_one_or_none()

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    patient.is_active = False

    db.commit()

    return