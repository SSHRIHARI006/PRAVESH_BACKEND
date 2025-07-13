# app/api/decrypt_qr_router.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_session
from app.utils.crypto_utils import decrypt_qr_data
from app.crud import user_crud, log_crud
from app.db.schemas import QRPayload

router = APIRouter(
    prefix="/qr",
    tags=["QR Decryption"]
)


@router.post("/decrypt")
async def decrypt_and_log(
        payload: QRPayload,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        data = decrypt_qr_data(payload.encrypted_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to decrypt: {str(e)}")

    qr_id = data.get("qr_id")
    if not qr_id:
        raise HTTPException(status_code=400, detail="Missing qr_id in QR data")

    user = await user_crud.get_user_by_bt_id(session, data["bt_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Process the scan type
    if payload.scan_type == "exit":
        await log_crud.create_exit_log(session, user_id=user.id, qr_id=qr_id)
    elif payload.scan_type == "entry":
        await log_crud.close_log_entry(session, qr_id=qr_id)
    elif payload.scan_type == "night_pass":
        # implement later
        pass
    else:
        raise HTTPException(status_code=400, detail="Invalid scan type")

    return {"message": f"{payload.scan_type} successfully logged."}
