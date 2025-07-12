from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.db.database import get_async_session
from app.utils.crypto_utils import decrypt_qr_data
from app.crud.user_crud import get_user_by_id
from app.crud.log_crud import create_exit_log, close_log_entry
from app.crud.log_leave_crud import create_log_leave
from app.db.schemas import LogCreate, LogLeaveCreate

router = APIRouter()


class QRPayload(BaseModel):
    encrypted_data: str
    scan_type: str  # e.g. "exit", "entry", "night_pass"


@router.post("/decrypt-qr")
async def decrypt_and_log(payload: QRPayload, session: AsyncSession = Depends(get_async_session)):
    try:
        data = decrypt_qr_data(payload.encrypted_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Decryption failed: {e}")

    # Check if this is a leave request
    if payload.scan_type == "night_pass":
        # Validate required fields
        missing_fields = [field for field in ["user_id", "bt_id", "reason_for_exit", "intended_return_date"]
                          if field not in data]
        if missing_fields:
            raise HTTPException(
                status_code=400,
                detail=f"Missing fields for night pass request: {missing_fields}"
            )

        # Optionally check if user exists
        user = await get_user_by_id(session, data["user_id"])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        leave_data = LogLeaveCreate(
            user_id=data["user_id"],
            bt_id=data["bt_id"],
            phone=user.phone,
            name=user.name,
            entry_timestamp=data.get("entry_timestamp", None),
            exit_timestamp=None,
            no_of_days=data.get("no_of_days"),
            additional_contact_info=data.get("additional_contact_info"),
            intended_location=data.get("intended_location"),
            intended_return_date=data.get("intended_return_date"),
            is_exit=False,
            is_hostel_user=user.is_hostel_user,
            hostel_room_no=user.hostel_room_no,
            reason_for_exit=data["reason_for_exit"],
            QR_ID=data.get("qr_id")
        )

        await create_log_leave(session, leave_data)
        return {"status": "success", "message": "Night pass leave request logged"}

    # Otherwise, it's a normal scan event
    qr_id = data.get("qr_id")
    user_id = data.get("user_id")

    if not qr_id or not user_id:
        raise HTTPException(status_code=400, detail="Missing qr_id or user_id in scan data")

    user = await get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if payload.scan_type == "exit":
        # Create new exit log
        log_data = LogCreate(
            user_id=user_id,
            qr_id=qr_id,
            type=data.get("log_type", "same_day"),  # default same_day if not specified
            timestamp_out=data.get("timestamp_out"),
            status="ongoing"
        )
        await create_exit_log(session, log_data)

    elif payload.scan_type == "entry":
        await close_log_entry(session, qr_id=qr_id)

    else:
        raise HTTPException(status_code=400, detail="Invalid scan type")

    return {"status": "success", "message": f"{payload.scan_type} processed successfully"}
