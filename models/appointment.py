from sqlalchemy import (
    String, Integer, Boolean, DateTime, ForeignKey, create_engine
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship, Session
)
from sqlalchemy.sql import func
from typing import Optional, List
from datetime import datetime
from database import Base

# class Base(DeclarativeBase):
#     pass

class Appointment(Base):
    __tablename__ = "appointments"
    # Your columns and relationships here
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    appointment_id: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False
    )

    patient_id: Mapped[str] = mapped_column(
        ForeignKey("patients.patient_id"),
        nullable=False
    )

    doctor_id: Mapped[str] = mapped_column(
        ForeignKey("doctors.doctor_id"),
        nullable=False
    )

    time_slot: Mapped[str] = mapped_column(
        String(5),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="Scheduled"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    patient: Mapped["Patient"] = relationship(
        back_populates = "appointments"
    )

    doctor: Mapped["Doctor"] = relationship(
        back_populates = "appointments"
    )

    def __repr__(self) -> str:
        return (
            f"Appointment("
            f"appointment_id='{self.appointment_id}', "
            f"patient_id='{self.patient_id}', "
            f"doctor_id='{self.doctor_id}', "
            f"status='{self.status}'"
            f")"
        )