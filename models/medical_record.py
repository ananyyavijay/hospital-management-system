from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from datetime import datetime

from database import Base

class MedicalRecord(Base):
    __tablename__ = "medical_records"
    id:          Mapped[int]           = mapped_column(Integer, primary_key=True)
    record_id:   Mapped[str]           = mapped_column(String(10), unique=True)
    patient_id:  Mapped[int]           = mapped_column(Integer, ForeignKey("patients.id"), nullable=False)
    filename:    Mapped[str]           = mapped_column(String(255))
    # file_path:   Mapped[str]           = mapped_column(String(500))
    blob_url:    Mapped[str]           = mapped_column(String(2000), nullable=False)
    # blob_url = Column(String(2000), nullable=False)
    file_type:   Mapped[str]           = mapped_column(String(50))
    size_kb:     Mapped[float]         = mapped_column(Float, default=0.0)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime)


