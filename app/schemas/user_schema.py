from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    bt_id: str
    email: EmailStr
    name: str
    phone: str
    gender: str
    hostel_room_no: Optional[int] = None
    is_hostel_user: bool = False
    is_admin: bool = False

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
