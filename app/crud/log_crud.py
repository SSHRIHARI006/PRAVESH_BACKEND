# app/crud/log_crud.py

from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import LogSameDay, LogLeave
from app.db.schemas import LogCreate

# -------------------------------
# Create an exit log
# -------------------------------

async def create_exit_log(session: AsyncSession, log_data: LogCreate):
    """
    Unified function to create an exit log in either log_same_day
    or log_leave table based on type field.
    """

    if log_data.type == "same_day":
        new_log = LogSameDay(
            QR_ID = log_data.qr_id,
            user_id = log_data.user_id,
            bt_id = log_data.bt_id,
            phone = log_data.phone,
            name = log_data.name,
            entry_timestamp = log_data.timestamp_out,
            exit_timestamp = None,
            is_exit = True,
            is_hostel_user = False,          # adjust if needed
            hostel_room_no = None,
            reason_for_exit = None
        )
        session.add(new_log)

    elif log_data.type == "leave":
        new_log = LogLeave(
            QR_ID = log_data.qr_id,
            user_id = log_data.user_id,
            bt_id = log_data.bt_id,
            phone = log_data.phone,
            name = log_data.name,
            entry_timestamp = log_data.timestamp_out,
            exit_timestamp = None,
            no_of_days = None,
            additional_contact_info = None,
            intended_location = None,
            intended_return_date = None,
            is_exit = True,
            is_hostel_user = False,
            hostel_room_no = None,
            reason_for_exit = None
        )
        session.add(new_log)

    else:
        raise ValueError("Invalid log type. Must be 'same_day' or 'leave'.")

    await session.commit()
    return {"status": "created"}

# ----------------------------------
# Find a log by QR_ID
# ----------------------------------

async def get_log_by_qr_id(session: AsyncSession, qr_id: str):
    """
    Check both log tables to see if this QR_ID already exists.
    """

    result_same_day = await session.execute(
        select(LogSameDay).where(LogSameDay.QR_ID == qr_id)
    )
    log_same_day = result_same_day.scalar_one_or_none()
    if log_same_day:
        return log_same_day

    result_leave = await session.execute(
        select(LogLeave).where(LogLeave.QR_ID == qr_id)
    )
    log_leave = result_leave.scalar_one_or_none()
    if log_leave:
        return log_leave

    return None

# -----------------------------------
# Close an existing log
# -----------------------------------

async def close_log_entry(session: AsyncSession, qr_id: str):
    """
    Close the log by setting exit_timestamp and status.
    """

    log = await get_log_by_qr_id(session, qr_id)

    if not log:
        return None

    log.exit_timestamp = datetime.utcnow()
    log.is_exit = False

    await session.commit()

    return log
