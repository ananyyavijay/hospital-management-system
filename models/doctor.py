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

class Base(DeclarativeBase):
    pass

class Doctor(Base):
    __tablename__ = "doctors"
    # Your columns and relationships here
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    doctor_id: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    specialization: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="doctor",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"Doctor("
            f"doctor_id='{self.doctor_id}', "
            f"name='{self.name}', "
            f"specialization='{self.specialization}'"
            f")"
        )