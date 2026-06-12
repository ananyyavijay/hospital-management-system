from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, Literal
from datetime import datetime
import re
from models.appointment import Appointment

class DoctorCreate(BaseModel):
    name: str = Field(..., min_length=3)
    specialization: str = Field(..., min_length=2)


# DoctorResponse
class DoctorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    # Your fields here
    doctor_id: str
    name: str
    specialization: str
    is_active: bool
    created_at: datetime