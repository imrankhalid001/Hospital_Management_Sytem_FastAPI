from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.database import Base


class Staff(Base):
    __tablename__ = "staff"
    
    id: Mapped [int] = mapped_column(primary_key=True)
    email: Mapped [str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped [str] = mapped_column(String(255))

class Patient(Base):
    
    __tablename__ = "patients"

    id: Mapped [int] = mapped_column(primary_key=True)
    name: Mapped [str] = mapped_column(String(200))
    age: Mapped [int] = mapped_column (Integer)
    gender: Mapped [str] = mapped_column(String(20))
    contact_number: Mapped [str] = mapped_column(String(20))
    diagnosis: Mapped [str] = mapped_column(String(500))
    doctor_assigned: Mapped [str] = mapped_column(String(200))
    admitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc))   
    registered_by_id: Mapped [int] = mapped_column(ForeignKey("staff.id"))