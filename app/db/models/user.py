from sqlalchemy import Column, Integer, String, Boolean
from app.db.session import Base

class User(Base):  
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    bt_id = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    gender = Column(String, nullable=False)  # male/female
    hostel_room_no = Column(Integer, nullable=True)
    is_hostel_user = Column(Boolean, nullable=False, default=False)
    is_admin = Column(Boolean, nullable=False, default=False) 