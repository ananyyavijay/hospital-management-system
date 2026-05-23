from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

class MedicalRecord(Base):
    __tablename__ = "medical_records"
    id:          Mapped[int]           = mapped_column(Integer, primary_key=True)
    record_id:   Mapped[str]           = mapped_column(String(10), unique=True)
    patient_id:  Mapped[str]           = mapped_column(String(10))
    filename:    Mapped[str]           = mapped_column(String(255))
    file_path:   Mapped[str]           = mapped_column(String(500))
    file_type:   Mapped[str]           = mapped_column(String(50))
    size_kb:     Mapped[float]         = mapped_column(Float, default=0.0)
    uploaded_at: Mapped[str]           = mapped_column(String(30))


