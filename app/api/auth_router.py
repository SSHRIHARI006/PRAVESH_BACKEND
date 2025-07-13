# app/api/auth_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import get_db
from app.crud import user_crud
from app.auth.jwt import create_access_token
from datetime import timedelta

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
):
    user = user_crud.verify_user_credentials(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_expires = timedelta(minutes=60)
    token = create_access_token(
        data={"sub": user.bt_id},
        expires_delta=token_expires,
    )

    return {"access_token": token, "token_type": "bearer"}
