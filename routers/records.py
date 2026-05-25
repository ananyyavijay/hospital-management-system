from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    status
)

from fastapi.responses import Response

from sqlalchemy.orm import Session
from sqlalchemy import select, func as sqlfunc

from pathlib import Path
from datetime import datetime
import shutil
import os

from database import get_db

from models.patient import Patient
from models.medical_record import MedicalRecord

from schemas.medical_record import (
    MedicalRecordResponse
)


router = APIRouter(
    tags=["Medical Records"]
)

UPLOAD_ROOT = Path("./uploads")


ALLOWED_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png"
}


def generate_record_id(db: Session):

    count = db.scalar(
        select(
            sqlfunc.count(MedicalRecord.id)
        )
    )

    return f"REC{count + 1:03d}"


@router.post(
    "/{patient_id}/records",
    response_model=MedicalRecordResponse,
    status_code=status.HTTP_201_CREATED
)
async def upload_record(
    patient_id: str,
    file: UploadFile = File(..., media_type="image/jpeg"),
    db: Session = Depends(get_db)
):

    # Check patient exists
    patient = db.scalar(
        select(Patient).where(
            Patient.patient_id == patient_id
        )
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # Validate file type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, JPEG and PNG allowed"
        )

    # Generate record ID
    record_id = generate_record_id(db)

    # Create patient folder
    patient_dir = UPLOAD_ROOT / patient_id

    patient_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # Final filename
    final_filename = (
        f"{record_id}_{file.filename}"
    )

    # Final path
    file_path = patient_dir / final_filename

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    # File size
    size_kb = round(
        os.path.getsize(file_path) / 1024,
        2
    )

    # Create DB record
    record = MedicalRecord(
        record_id=record_id,
        patient_id=patient_id,
        filename=file.filename,
        file_path=str(file_path),
        file_type=file.content_type,
        size_kb=size_kb,
        uploaded_at=datetime.now()
    )

    db.add(record)

    db.commit()

    db.refresh(record)

    return record


@router.get(
    "/{patient_id}/records",
    response_model=list[MedicalRecordResponse]
)
def list_records(
    patient_id: str,
    db: Session = Depends(get_db)
):

    patient = db.scalar(
        select(Patient).where(
            Patient.patient_id == patient_id
        )
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    records = db.scalars(
        select(MedicalRecord).where(
            MedicalRecord.patient_id == patient_id
        )
    ).all()

    return records


@router.delete(
    "/{patient_id}/records/{record_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_record(
    patient_id: str,
    record_id: str,
    db: Session = Depends(get_db)
):

    patient = db.scalar(
        select(Patient).where(
            Patient.patient_id == patient_id
        )
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    record = db.scalar(
        select(MedicalRecord).where(
            MedicalRecord.record_id == record_id,
            MedicalRecord.patient_id == patient_id
        )
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Medical record not found"
        )

    # Delete file from disk
    if os.path.exists(record.file_path):
        os.remove(record.file_path)

    # Delete DB record
    db.delete(record)

    db.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )