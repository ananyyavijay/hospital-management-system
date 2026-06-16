from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from database import Base
from models.appointment import Appointment


# ✏️ Write Patient model
class Patient(Base):
    __tablename__ = "patients"
    # Your columns and relationships here
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    patient_id: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    blood_group: Mapped[str] = mapped_column(String(5), nullable=False)

    age: Mapped[int] = mapped_column(Integer, default=0)

    contact: Mapped[str | None] = mapped_column(String(15), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="patient", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"Patient("
            f"patient_id='{self.patient_id}', "
            f"name='{self.name}', "
            f"blood_group='{self.blood_group}'"
            f")"
        )
