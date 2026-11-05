from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routers import patients, staff



@asynccontextmanager
async def lifespan (app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    
app = FastAPI(title="Hospital Patient Management API", lifespan = lifespan)

app.include_router(staff.router)
app.include_router(patients.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Hospital Patient Management API"}    