from pydantic import BaseModel, ConfigDict
from datetime import datetime


class MedicalRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    record_id: str
    patient_id: str
    filename: str
    file_type: str
    size_kb: float
    uploaded_at: datetime