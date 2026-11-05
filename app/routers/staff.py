from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.auth import get_current_staff
from app.models import Staff
from app.schemas import StaffCreate, Token
from app.auth import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter(prefix="/staff", tags=["Staff"])

@router.post("signup", status_code=201)
async def signup(staff: StaffCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Staff).where(Staff.email == staff.email))
    if result.scalar_one_or_none() is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_staff = Staff(email=staff.email, password=hash_password(staff.password))
    db.add(new_staff)
    await db.commit()
    return {"message": "Staff registered successfully"}


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession =  Depends(get_db)):
    result = await db.execute(select(Staff).where(Staff.email == form_data.username))
    staff = result.scalar_one_or_none()
    if staff is None or not verify_password(form_data.password, staff.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(data={"sub": staff.email})
    return Token(access_token=token)