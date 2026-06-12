from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime

class DashboardPatientInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    patient_id: str
    name: str
    blood_group: str
    age: int


class DashboardAppointment(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    appointment_id: str
    doctor_name: str
    time_slot: str
    status: str


class DashboardRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    record_id: str
    filename: str
    file_type: str
    uploaded_at: datetime


class DashboardStats(BaseModel):
    total_appointments: int
    completed_appointments: int
    upcoming_count: int


class PatientDashboardResponse(BaseModel):
    patient: DashboardPatientInfo
    upcoming_appointments: List[DashboardAppointment]
    past_appointments: List[DashboardAppointment]
    medical_records: List[DashboardRecord]
    stats: DashboardStats
