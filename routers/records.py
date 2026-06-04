# from fastapi import (
#     APIRouter,
#     Depends,
#     HTTPException,
#     UploadFile,
#     File,
#     status
# )

# from fastapi.responses import Response

# from sqlalchemy.orm import Session
# from sqlalchemy import select, func as sqlfunc

# from pathlib import Path
# from datetime import datetime
# import shutil
# import os

# from database import get_db

# from models.patient import Patient
# from models.medical_record import MedicalRecord

# from schemas.medical_record import (
#     MedicalRecordResponse
# )


# router = APIRouter(
#     tags=["Medical Records"]
# )

# UPLOAD_ROOT = Path(
#     os.getenv("UPLOAD_DIR", "./uploads")
# )


# ALLOWED_TYPES = {
#     "application/pdf",
#     "image/jpeg",
#     "image/png"
# }


# def generate_record_id(db: Session):

#     count = db.scalar(
#         select(
#             sqlfunc.count(MedicalRecord.id)
#         )
#     )

#     return f"REC{count + 1:03d}"


# @router.post(
#     "/{patient_id}/records",
#     response_model=MedicalRecordResponse,
#     status_code=status.HTTP_201_CREATED
# )
# async def upload_record(
#     patient_id: str,
#     file: UploadFile = File(..., media_type="image/jpeg"),
#     db: Session = Depends(get_db)
# ):

#     # Check patient exists
#     patient = db.scalar(
#         select(Patient).where(
#             Patient.patient_id == patient_id
#         )
#     )

#     if not patient:
#         raise HTTPException(
#             status_code=404,
#             detail="Patient not found"
#         )

#     # Validate file type
#     if file.content_type not in ALLOWED_TYPES:
#         raise HTTPException(
#             status_code=400,
#             detail="Only PDF, JPEG and PNG allowed"
#         )

#     # Generate record ID
#     record_id = generate_record_id(db)

#     # Create patient folder
#     patient_dir = UPLOAD_ROOT / patient_id

#     patient_dir.mkdir(
#         parents=True,
#         exist_ok=True
#     )

#     # Final filename
#     final_filename = (
#         f"{record_id}_{file.filename}"
#     )

#     # Final path
#     file_path = patient_dir / final_filename

#     # Save file
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(
#             file.file,
#             buffer
#         )

#     # File size
#     size_kb = round(
#         os.path.getsize(file_path) / 1024,
#         2
#     )

#     # Create DB record
#     record = MedicalRecord(
#         record_id=record_id,
#         patient_id=patient_id,
#         filename=file.filename,
#         file_path=str(file_path),
#         file_type=file.content_type,
#         size_kb=size_kb,
#         uploaded_at=datetime.now()
#     )

#     db.add(record)

#     db.commit()

#     db.refresh(record)

#     return record


# @router.get(
#     "/{patient_id}/records",
#     response_model=list[MedicalRecordResponse]
# )
# def list_records(
#     patient_id: str,
#     db: Session = Depends(get_db)
# ):

#     patient = db.scalar(
#         select(Patient).where(
#             Patient.patient_id == patient_id
#         )
#     )

#     if not patient:
#         raise HTTPException(
#             status_code=404,
#             detail="Patient not found"
#         )

#     records = db.scalars(
#         select(MedicalRecord).where(
#             MedicalRecord.patient_id == patient_id
#         )
#     ).all()

#     return records


# @router.delete(
#     "/{patient_id}/records/{record_id}",
#     status_code=status.HTTP_204_NO_CONTENT
# )
# def delete_record(
#     patient_id: str,
#     record_id: str,
#     db: Session = Depends(get_db)
# ):

#     patient = db.scalar(
#         select(Patient).where(
#             Patient.patient_id == patient_id
#         )
#     )

#     if not patient:
#         raise HTTPException(
#             status_code=404,
#             detail="Patient not found"
#         )

#     record = db.scalar(
#         select(MedicalRecord).where(
#             MedicalRecord.record_id == record_id,
#             MedicalRecord.patient_id == patient_id
#         )
#     )

#     if not record:
#         raise HTTPException(
#             status_code=404,
#             detail="Medical record not found"
#         )

#     # Delete file from disk
#     if os.path.exists(record.file_path):
#         os.remove(record.file_path)

#     # Delete DB record
#     db.delete(record)

#     db.commit()

#     return Response(
#         status_code=status.HTTP_204_NO_CONTENT
#     )

import os
import logging
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.medical_record import MedicalRecord
from models.patient import Patient
from schemas.medical_record  import MedicalRecordOut, RecordDownloadOut 

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/patients", tags=["Records"])

# ── Blob Storage config ───────────────────────────────────────────────────────
STORAGE_ACCOUNT = os.getenv("STORAGE_ACCOUNT_NAME", "")
CONTAINER       = os.getenv("BLOB_CONTAINER_NAME",  "hmsmedicalrecords")
ACCOUNT_URL     = f"https://{STORAGE_ACCOUNT}.blob.core.windows.net"
APP_ENV         = os.getenv("APP_ENV", "development")

ALLOWED_TYPES = {"application/pdf", "image/jpeg", "image/png"}


def _get_blob_service_client():
    """Return an authenticated BlobServiceClient.
    Uses Managed Identity on Azure, falls back to connection string locally."""
    from azure.storage.blob import BlobServiceClient
    if APP_ENV == "production":
        from azure.identity import ManagedIdentityCredential
        return BlobServiceClient(
            account_url=ACCOUNT_URL,
            credential=ManagedIdentityCredential()
        )
    else:
        # Local dev: use connection string from .env
        conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
        if conn_str:
            return BlobServiceClient.from_connection_string(conn_str)
        raise RuntimeError(
            "Set AZURE_STORAGE_CONNECTION_STRING in .env for local dev, "
            "or set APP_ENV=production to use Managed Identity."
        )


def _upload_to_blob(content: bytes, blob_name: str) -> str:
    """Upload bytes to Blob Storage. Returns the plain blob URL."""
    client = _get_blob_service_client()
    blob_client = client.get_blob_client(container=CONTAINER, blob=blob_name)
    blob_client.upload_blob(content, overwrite=True)
    logger.info("Uploaded blob: %s", blob_name)
    return blob_client.url


def _generate_sas_url(blob_name: str, expiry_minutes: int = 60) -> str:
    """Generate a user delegation SAS URL valid for expiry_minutes."""
    from azure.storage.blob import BlobSasPermissions, generate_blob_sas
    client = _get_blob_service_client()
    now    = datetime.now(timezone.utc)
    expiry = now + timedelta(minutes=expiry_minutes)
    key = client.get_user_delegation_key(
        key_start_time=now,
        key_expiry_time=expiry
    )
    sas = generate_blob_sas(
        account_name=STORAGE_ACCOUNT,
        container_name=CONTAINER,
        blob_name=blob_name,
        user_delegation_key=key,
        permission=BlobSasPermissions(read=True),
        expiry=expiry,
    )
    return f"{ACCOUNT_URL}/{CONTAINER}/{blob_name}?{sas}"


def _blob_name(patient_id: str, record_id: str, filename: str) -> str:
    """Construct a consistent blob name for a medical record."""
    return f"{patient_id}/{record_id}_{filename}"


# ── Endpoints ─────────────────────────────────────────────────────────────────
@router.post("/{patient_id}/records",
    response_model=MedicalRecordOut, status_code=201)
async def upload_record(
    patient_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a medical record file to Azure Blob Storage."""
    # Validate patient
    patient = db.scalars(select(Patient).where(
        Patient.patient_id == patient_id,
        Patient.is_active == True
    )).first()
    if not patient:
        raise HTTPException(404, f"Patient {patient_id} not found")

    # Validate file type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400,
            f"File type {file.content_type!r} not allowed. Use PDF, JPEG or PNG.")

    # Read file content
    content = await file.read()
    size_kb = round(len(content) / 1024, 2)

    # Generate record ID
    count = db.scalar(select(func.count(MedicalRecord.id))) or 0
    record_id = f"REC{count + 1:03d}"

    # Upload to Blob Storage
    blob_name = _blob_name(patient_id, record_id, file.filename)
    try:
        blob_url = _upload_to_blob(content, blob_name)
    except Exception as e:
        logger.exception("Blob upload failed")
        raise HTTPException(
            status_code=500,
            detail=f"Blob upload failed: {str(e)}"
        )

    # Save metadata to DB
    record = MedicalRecord(
        record_id   = record_id,
        patient_id  = patient.id,
        filename    = file.filename,
        blob_url    = blob_url,
        file_type   = file.content_type,
        size_kb     = size_kb,
        uploaded_at = datetime.now(timezone.utc),
    )
    try:
        db.add(record)
        db.commit()
        db.refresh(record)
    except Exception as e:
        db.rollback()
        logger.exception("Database insert failed")
        raise HTTPException(
            status_code=500,
            detail=f"Database insert failed: {str(e)}"
        )
    return record


@router.get("/{patient_id}/records", response_model=List[MedicalRecordOut])
def list_records(
    patient_id: str,
    db: Session = Depends(get_db)
):
    """List all medical records for a patient (metadata only — no file content)."""
    patient = db.scalars(select(Patient).where(
        Patient.patient_id == patient_id,
        Patient.is_active == True
    )).first()
    if not patient:
        raise HTTPException(404, f"Patient {patient_id} not found")
    return db.scalars(
        select(MedicalRecord).where(MedicalRecord.patient_id == patient.id)
    ).all()


@router.get("/{patient_id}/records/{record_id}/download",
            response_model=RecordDownloadOut)
def download_record(
    patient_id: str,
    record_id:  str,
    db: Session = Depends(get_db)
):
    """Generate a time-limited SAS download URL for a medical record."""
    patient = db.scalars(
        select(Patient).where(
            Patient.patient_id == patient_id
        )
    ).first()

    if not patient:
        raise HTTPException(404, "Patient not found")

    record = db.scalars(
        select(MedicalRecord).where(
            MedicalRecord.record_id == record_id,
            MedicalRecord.patient_id == patient.id
        )
    ).first()
    
    if not record:
        raise HTTPException(404, f"Record {record_id} not found")

    blob_name    = _blob_name(patient_id, record_id, record.filename)
    download_url = _generate_sas_url(blob_name, expiry_minutes=60)

    return RecordDownloadOut(
        record_id    = record_id,
        filename     = record.filename,
        download_url = download_url,
        expires_in   = "60 minutes",
    )
