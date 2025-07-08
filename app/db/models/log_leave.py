from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.db.session import Base

class LogLeave(Base):
    __tablename__ = "log_leave"

    index = Column(Integer, primary_key=True, index=True)
    QR_ID = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    bt_id = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    name = Column(String, nullable=False)
    entry_timestamp = Column(DateTime, nullable=False)
    exit_timestamp = Column(DateTime, nullable=True)
    no_of_days = Column(Integer, nullable=True)
    additional_contact_info = Column(String, nullable=True)
    intended_location = Column(String, nullable=True)
    intended_return_date = Column(DateTime, nullable=True)
    is_exit = Column(Boolean, nullable=False, default=False)
    is_hostel_user = Column(Boolean, nullable=False, default=False)
    hostel_room_no = Column(Integer, nullable=True)
    reason_for_exit = Column(String, nullable=True)
