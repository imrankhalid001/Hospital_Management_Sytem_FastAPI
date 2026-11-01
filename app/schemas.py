from pydantic import BaseModel, ConfigDict
from datetime import datetime


class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str
    contact_number: str
    diagnosis: str
    doctor_assigned: str

class PatientOut(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    contact_number: str
    diagnosis: str
    doctor_assigned: str
    admitted_at: datetime



model_config = ConfigDict(from_attributes=True)