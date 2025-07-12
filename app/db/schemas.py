# app/db/schemas.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LogCreate(BaseModel):
    user_id: int
    qr_id: str
    bt_id: str
    phone: str
    name: str
    timestamp_out: datetime
    status: str
    type: str    # either "same_day" or "leave"



class LogLeaveCreate(BaseModel):
    user_id: int
    bt_id: str
    phone: str
    name: str
    entry_timestamp: Optional[datetime] = None
    exit_timestamp: Optional[datetime] = None
    no_of_days: Optional[int] = None
    additional_contact_info: Optional[str] = None
    intended_location: Optional[str] = None
    intended_return_date: Optional[datetime] = None
    is_exit: bool = False
    is_hostel_user: bool = False
    hostel_room_no: Optional[int] = None
    reason_for_exit: Optional[str] = None
    QR_ID: Optional[str] = None
