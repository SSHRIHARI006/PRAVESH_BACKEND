# app/api/users_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud import user_crud
from app.db.models import User
from app.auth.jwt import get_current_user
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post("/", response_model=User)
def create_user(user: User, db: Session = Depends(get_db)):
    return user_crud.create_user(db, user)

@router.get("/", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, updates: dict, db: Session = Depends(get_db)):
    user = user_crud.update_user(db, user_id, updates)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    result = user_crud.delete_user(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
