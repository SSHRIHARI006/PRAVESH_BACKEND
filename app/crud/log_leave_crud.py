# app/crud/log_leave_crud.py

from sqlalchemy.orm import Session
from app.db.models import LogLeave

def create_leave_log(db: Session, log: LogLeave) -> LogLeave:
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def get_leave_log_by_qr_id(db: Session, qr_id: str) -> LogLeave | None:
    return db.query(LogLeave).filter(LogLeave.QR_ID == qr_id).first()

def update_leave_return_info(db: Session, qr_id: str, entry_time, return_location) -> LogLeave | None:
    log = get_leave_log_by_qr_id(db, qr_id)
    if log:
        log.entry_timestamp = entry_time
        log.intended_location = return_location  # if needed to update
        db.commit()
        db.refresh(log)
    return log

def get_leave_logs_by_user(db: Session, user_id: int) -> list[LogLeave]:
    return db.query(LogLeave).filter(LogLeave.user_id == user_id).all()

def delete_leave_log(db: Session, qr_id: str) -> bool:
    log = get_leave_log_by_qr_id(db, qr_id)
    if log:
        db.delete(log)
        db.commit()
        return True
    return False
