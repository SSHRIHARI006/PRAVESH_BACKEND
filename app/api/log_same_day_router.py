# app/api/log_same_day_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import LogSameDay
from app.crud.log_same_day_crud import (
    create_log_same_day,
    get_log_same_day_by_qr_id,
    get_all_log_same_day,
    update_log_same_day,
    delete_log_same_day,
)
from typing import List

router = APIRouter(
    prefix="/logs/same-day",
    tags=["LogSameDay"],
)

@router.post("/", response_model=LogSameDay)
def create_log(log: LogSameDay, db: Session = Depends(get_db)):
    return create_log_same_day(db, log)

@router.get("/", response_model=List[LogSameDay])
def read_logs(db: Session = Depends(get_db)):
    return get_all_log_same_day(db)

@router.get("/{qr_id}", response_model=LogSameDay)
def read_log(qr_id: str, db: Session = Depends(get_db)):
    log = get_log_same_day_by_qr_id(db, qr_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log

@router.put("/{qr_id}", response_model=LogSameDay)
def update_log(qr_id: str, updates: dict, db: Session = Depends(get_db)):
    updated = update_log_same_day(db, qr_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Log not found")
    return updated

@router.delete("/{qr_id}")
def delete_log(qr_id: str, db: Session = Depends(get_db)):
    result = delete_log_same_day(db, qr_id)
    if not result:
        raise HTTPException(status_code=404, detail="Log not found")
    return {"message": "Log deleted successfully"}
