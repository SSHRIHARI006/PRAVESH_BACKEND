# app/db/database.py

import os
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import create_engine
from collections.abc import AsyncGenerator

DATABASE_URL = os.getenv("DATABASE_URL")

# -------------------------------
# Sync Engine + Session
# -------------------------------

# Create sync engine
engine = create_engine(DATABASE_URL, echo=True)

# Sync session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Sync session dependency
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------
# Async Engine + Session
# -------------------------------

# Create async engine
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Async session factory
async_session_maker = sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Async session dependency
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
