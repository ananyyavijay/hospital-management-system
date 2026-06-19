from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from database import Base
from models.appointment import Appointment


class Doctor(Base):
    __tablename__ = "doctors"
    # Your columns and relationships here
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    doctor_id: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    specialization: Mapped[str] = mapped_column(String(100), nullable=False)

    availability: Mapped[dict] = mapped_column(JSON, default=dict)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # available_slots: Mapped[list] = mapped_column(JSON, default=list)

    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="doctor", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"Doctor("
            f"doctor_id='{self.doctor_id}', "
            f"name='{self.name}', "
            f"specialization='{self.specialization}'"
            f")"
        )
