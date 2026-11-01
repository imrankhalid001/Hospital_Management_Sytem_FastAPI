from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine, Base
from app import models


@asynccontextmanager
async def lifespan (app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    
app = FastAPI(title="Hospital Patient Management API", lifespan = lifespan)