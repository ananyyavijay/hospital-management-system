from pydantic import BaseModel, ConfigDict
from datetime import datetime


# class MedicalRecordResponse(BaseModel):
#     model_config = ConfigDict(from_attributes=True)

#     record_id: str
#     patient_id: str
#     filename: str
#     file_type: str
#     size_kb: float
#     uploaded_at: datetime

class MedicalRecordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    record_id:   str
    patient_id:  str
    filename:    str
    file_type:   str
    size_kb:     float
    uploaded_at: datetime
    # blob_url intentionally not returned — use /download to get SAS URL


class RecordDownloadOut(BaseModel):
    record_id:    str
    filename:     str
    download_url: str   # time-limited SAS URL
    expires_in:   str   # e.g. "60 minutes"