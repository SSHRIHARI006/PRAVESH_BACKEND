# app/crud/log_leave_crud.py

from sqlmodel import select
from app.db.models import LogLeave
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import datetime

# CREATE
async def create_log_leave(
    session: AsyncSession,
    log_data: LogLeave
) -> LogLeave:
    session.add(log_data)
    await session.commit()
    await session.refresh(log_data)
    return log_data


# READ ALL
async def get_all_logs_leave(session: AsyncSession) -> list[LogLeave]:
    result = await session.execute(select(LogLeave))
    return result.scalars().all()


# READ BY ID
async def get_log_leave_by_id(session: AsyncSession, log_id: UUID) -> LogLeave | None:
    result = await session.execute(
        select(LogLeave).where(LogLeave.log_id == log_id)
    )
    return result.scalar_one_or_none()


# READ BY USER_ID
async def get_logs_leave_by_user(session: AsyncSession, user_id: UUID) -> list[LogLeave]:
    result = await session.execute(
        select(LogLeave).where(LogLeave.user_id == user_id)
    )
    return result.scalars().all()


# UPDATE TIMESTAMP_IN
async def update_timestamp_in_leave(
    session: AsyncSession,
    log_id: UUID,
    timestamp_in: datetime
) -> LogLeave | None:
    log = await get_log_leave_by_id(session, log_id)
    if log:
        log.timestamp_in = timestamp_in
        await session.commit()
        await session.refresh(log)
    return log


# UPDATE STATUS
async def update_status_leave(
    session: AsyncSession,
    log_id: UUID,
    status: str
) -> LogLeave | None:
    log = await get_log_leave_by_id(session, log_id)
    if log:
        log.status = status
        await session.commit()
        await session.refresh(log)
    return log


# DELETE
async def delete_log_leave(session: AsyncSession, log_id: UUID) -> bool:
    log = await get_log_leave_by_id(session, log_id)
    if log:
        await session.delete(log)
        await session.commit()
        return True
    return False


async def create_night_pass(session: AsyncSession, user_id: str) -> None:
    new_leave = LogLeave(
        user_id=user_id,
        reason="Night Pass",
        from_date=None,
        to_date=None,
        approved=True,
        remarks="Night pass QR scan"
    )
    session.add(new_leave)
    await session.commit()