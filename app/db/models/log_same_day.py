from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.db.session import Base

class LogSameDay(Base):
    __tablename__ = "log_same_day"

    index = Column(Integer, primary_key=True, index=True)
    QR_ID = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    bt_id = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    name = Column(String, nullable=False)
    entry_timestamp = Column(DateTime, nullable=False)
    exit_timestamp = Column(DateTime, nullable=True)
    is_exit = Column(Boolean, nullable=False, default=False)
    is_hostel_user = Column(Boolean, nullable=False, default=False)
    hostel_room_no = Column(Integer, nullable=True)
    reason_for_exit = Column(String, nullable=True)
