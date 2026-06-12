from pydantic import BaseModel, ConfigDict
from typing import Generic, TypeVar, List


T = TypeVar("T")


# ── Generic Pagination Response ──────────────────────────────────────────────

class PaginatedResponse(
    BaseModel,
    Generic[T]
):
    total: int
    page: int
    limit: int
    pages: int
    data: List[T]


# ── Patient Output ────────────────────────────────────────────────────────────

class AdminPatientOut(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    patient_id: str
    name: str
    blood_group: str
    is_active: bool


# ── Doctor Output ─────────────────────────────────────────────────────────────

class AdminDoctorOut(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    doctor_id: str
    name: str
    specialization: str
    is_active: bool


# ── Appointment Output ────────────────────────────────────────────────────────

class AdminAppointmentOut(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    appointment_id: str
    patient_id: str
    doctor_id: str
    time_slot: str
    status: str


# ── Stats Output ──────────────────────────────────────────────────────────────

class AdminStatsOut(BaseModel):
    total_patients: int
    active_patients: int
    total_doctors: int
    total_appointments: int

    by_status: dict