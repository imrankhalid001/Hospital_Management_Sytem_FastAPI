from select import select

from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.models import Patient, Staff
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import PatientOut, PatientCreate
from app.auth import get_current_staff
from app.database import get_db
from sqlalchemy import select


router = APIRouter(prefix="/patients" , tags = ["patients"])

@router.post("/" , response_model=PatientOut, status_code=201)
async def create_patient(patient: PatientCreate, 
    db: AsyncSession = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff)
    ):
    new_patient = Patient(**patient.model_dump(), registered_by_id=current_staff.id)
    db.add(new_patient)
    await db.commit()
    await db.refresh(new_patient)
    return new_patient


@router.get("/", list=PatientOut)
async def list_patients(db: AsyncSession = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff)
    ):
    result = await db.execute(select(Patient))
    return result.scalars().all()


@router.get("/{patient_id}", response_model=PatientOut)
async def get_patient(patient_id: int, db: AsyncSession = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff)
    ):
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    patient = result.scalar_one_or_none()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient



@router.put("/{patient_id}", response_model=PatientOut)
async def update_patient(patient_id: int, updated: PatientCreate, db: AsyncSession = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff)
    ):
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    existing_patient = result.scalar_one_or_none()
    if existing_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    for field, value in updated.model_dump().items():
        setattr(existing_patient, field, value)
    await db.commit()
    await db.refresh(existing_patient)
    return existing_patient


@router.delete("/{patient_id}", status_code=204)
async def delete_patient(patient_id: int, db: AsyncSession = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff)
    ):
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    existing_patient = result.scalar_one_or_none()
    
    if existing_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    await db.delete(existing_patient)
    await db.commit()
    return None