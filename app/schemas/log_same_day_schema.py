from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LogSameDayBase(BaseModel):
    QR_ID: str
    user_id: int
    bt_id: str
    phone: str
    name: str
    entry_timestamp: datetime
    exit_timestamp: Optional[datetime] = None
    is_exit: bool = False
    is_hostel_user: bool = False
    hostel_room_no: Optional[int] = None
    reason_for_exit: Optional[str] = None

class LogSameDayCreate(LogSameDayBase):
    pass

class LogSameDayOut(LogSameDayBase):
    index: int

    class Config:
        orm_mode = True
