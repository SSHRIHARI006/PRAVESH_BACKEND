# app/crud/log_same_day_crud.py

from sqlmodel import select
from app.db.models import LogSameDay
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.db.models import LogSameDay

# CREATE
async def create_log_same_day(
    session: AsyncSession,
    log_data: LogSameDay
) -> LogSameDay:
    session.add(log_data)
    await session.commit()
    await session.refresh(log_data)
    return log_data


# READ ALL
async def get_all_logs_same_day(session: AsyncSession) -> list[LogSameDay]:
    result = await session.execute(select(LogSameDay))
    return result.scalars().all()


# READ BY ID
async def get_log_same_day_by_id(session: AsyncSession, log_id: UUID) -> LogSameDay | None:
    result = await session.execute(
        select(LogSameDay).where(LogSameDay.log_id == log_id)
    )
    return result.scalar_one_or_none()


# READ BY USER_ID
async def get_logs_same_day_by_user(session: AsyncSession, user_id: UUID) -> list[LogSameDay]:
    result = await session.execute(
        select(LogSameDay).where(LogSameDay.user_id == user_id)
    )
    return result.scalars().all()


# UPDATE TIMESTAMP_IN
async def update_timestamp_in_same_day(
    session: AsyncSession,
    log_id: UUID,
    timestamp_in: datetime
) -> LogSameDay | None:
    log = await get_log_same_day_by_id(session, log_id)
    if log:
        log.timestamp_in = timestamp_in
        await session.commit()
        await session.refresh(log)
    return log


# UPDATE STATUS
async def update_status_same_day(
    session: AsyncSession,
    log_id: UUID,
    status: str
) -> LogSameDay | None:
    log = await get_log_same_day_by_id(session, log_id)
    if log:
        log.status = status
        await session.commit()
        await session.refresh(log)
    return log


# DELETE
async def delete_log_same_day(session: AsyncSession, log_id: UUID) -> bool:
    log = await get_log_same_day_by_id(session, log_id)
    if log:
        await session.delete(log)
        await session.commit()
        return True
    return False


async def close_log_entry(session: AsyncSession, user_id: str) -> None:
    # Find any log with open status for this user
    stmt = (
        select(LogSameDay)
        .where(
            LogSameDay.user_id == user_id,
            LogSameDay.status == "open"
        )
    )
    result = await session.execute(stmt)
    log = result.scalars().first()

    if log:
        # Update status to closed
        upd = (
            update(LogSameDay)
            .where(LogSameDay.id == log.id)
            .values(status="closed")
        )
        await session.execute(upd)
        await session.commit()