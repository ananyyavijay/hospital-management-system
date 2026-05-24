from pydantic import BaseModel, ConfigDict
from typing import Generic, TypeVar, List


T = TypeVar("T")


class PaginatedResponse(
    BaseModel,
    Generic[T]
):
    total: int
    page: int
    limit: int
    pages: int
    data: List[T]


class AdminPatientOut(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    patient_id: str
    name: str
    blood_group: str
    is_active: bool


class AdminDoctorOut(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    doctor_id: str
    name: str
    specialization: str
    is_active: bool


class AdminAppointmentOut(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    appointment_id: str
    patient_id: str
    doctor_id: str
    time_slot: str
    status: str


class AdminStatsOut(BaseModel):
    total_patients: int
    active_patients: int
    total_doctors: int
    total_appointments: int

    by_status: dict