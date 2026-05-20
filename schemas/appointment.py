from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, Literal
from datetime import datetime
import re

class AppointmentCreate(BaseModel):
    # Your fields here — include slot format validator
    patient_id: str
    doctor_id: str
    time_slot: str
    status: str = "Scheduled"
    
    @field_validator("time_slot")
    @classmethod
    def validate_time_slot(cls, value):
        pattern = r"^\d{2}:\d{2}$"

        if not re.match(pattern, value):
            raise ValueError("time_slot must be in HH:MM format")

        return value
                     

# ✏️ AppointmentResponse
class AppointmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    # Your fields here — include optional patient_name and doctor_name
    appointment_id: str
    patient_id: str
    doctor_id: str
    time_slot: str
    status: str
    created_at: datetime
    patient_name: Optional[str] = None
    doctor_name: Optional[str] = None