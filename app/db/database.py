# app/db/database.py

from sqlmodel import  create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Sync engine (optional if you only want async)
engine = create_engine(DATABASE_URL, echo=True)

# Async engine (recommended)
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Async session factory
async_session_maker = sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Dependency to use in FastAPI routes
async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
