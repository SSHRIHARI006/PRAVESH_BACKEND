# app/crud/log_same_day_crud.py

from sqlalchemy.orm import Session
from app.db.models import LogSameDay

def create_log(db: Session, log: LogSameDay) -> LogSameDay:
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def get_log_by_qr_id(db: Session, qr_id: str) -> LogSameDay | None:
    return db.query(LogSameDay).filter(LogSameDay.QR_ID == qr_id).first()

def update_log_entry_time(db: Session, qr_id: str, entry_time) -> LogSameDay | None:
    log = get_log_by_qr_id(db, qr_id)
    if log:
        log.entry_timestamp = entry_time
        db.commit()
        db.refresh(log)
    return log

def get_logs_by_user(db: Session, user_id: int) -> list[LogSameDay]:
    return db.query(LogSameDay).filter(LogSameDay.user_id == user_id).all()

def delete_log(db: Session, qr_id: str) -> bool:
    log = get_log_by_qr_id(db, qr_id)
    if log:
        db.delete(log)
        db.commit()
        return True
    return False
