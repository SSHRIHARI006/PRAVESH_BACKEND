from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

# -----------------------
# User Model
# -----------------------

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    bt_id: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    password: str
    name: str
    phone: str
    gender: str
    hostel_room_no: Optional[int] = None
    is_hostel_user: bool = False
    is_admin: bool = False


# -----------------------
# LogSameDay Model
# -----------------------

class LogSameDay(SQLModel, table=True):
    __tablename__ = "log_same_day"

    index: Optional[int] = Field(default=None, primary_key=True)
    QR_ID: str = Field(unique=True)
    user_id: int = Field(foreign_key="users.id")
    bt_id: str
    phone: str
    name: str
    entry_timestamp: datetime
    exit_timestamp: Optional[datetime] = None
    is_exit: bool = False
    is_hostel_user: bool = False
    hostel_room_no: Optional[int] = None
    reason_for_exit: Optional[str] = None


# -----------------------
# LogLeave Model
# -----------------------

class LogLeave(SQLModel, table=True):
    __tablename__ = "log_leave"

    index: Optional[int] = Field(default=None, primary_key=True)
    QR_ID: str = Field(unique=True)
    user_id: int = Field(foreign_key="users.id")
    bt_id: str
    phone: str
    name: str
    entry_timestamp: datetime
    exit_timestamp: Optional[datetime] = None
    no_of_days: Optional[int] = None
    additional_contact_info: Optional[str] = None
    intended_location: Optional[str] = None
    intended_return_date: Optional[datetime] = None
    is_exit: bool = False
    is_hostel_user: bool = False
    hostel_room_no: Optional[int] = None
    reason_for_exit: Optional[str] = None
