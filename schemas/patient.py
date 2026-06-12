from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, Literal
from datetime import datetime
import re
from models.appointment import Appointment

VALID_BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

# PatientCreate
class PatientCreate(BaseModel):
    # Your fields here
    name: str = Field(..., min_length=2)
    blood_group: str
    age: int = Field(default=0, ge=0)
    contact: Optional[str] = None

    @field_validator("blood_group")
    @classmethod
    def validate_blood_group(cls, value):
        if value not in VALID_BLOOD_GROUPS:
            raise ValueError("Invalid Blood Group")
        return value

# PatientResponse
class PatientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    # Your fields here
    patient_id: str
    name: str
    blood_group: str
    age: int
    contact: Optional[str] = None
    is_active: bool
    created_at: datetime
