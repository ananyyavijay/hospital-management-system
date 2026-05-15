from dataclasses import dataclass, field, replace
from typing import ClassVar
from models.patient import Patient
from models.doctor import Doctor

@dataclass(frozen=True)
class Appointment:
    """Immutable appointment record."""
    _counter: ClassVar[int] = 0

    patient: Patient
    doctor: Doctor
    time_slot: str
    status: str = "Scheduled"
    appointment_id: str = field(init=False)

    def __post_init__(self) -> None:
        Appointment._counter += 1

        object.__setattr__(
            self,
            "appointment_id",
            f"APT{Appointment._counter:04d}"
        )

    def cancel(self) -> 'Appointment':
        # ✏️ Return a new Appointment with status='Cancelled'
        return replace(self, status = 'Cancelled')

    def __str__(self) -> str:
        # ✏️ Clean summary string
        return (
            f"Appointment ID: {self.appointment_id}\n"
            f"Patient       : {self.patient.name}\n"
            f"Doctor        : {self.doctor.name}\n"
            f"Time Slot     : {self.time_slot}\n"
            f"Status        : {self.status}"
        )