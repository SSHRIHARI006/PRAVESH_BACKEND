from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from app.db.database import get_async_session
from app.crud.user_crud import get_user_by_email
from app.core.auth import verify_password, create_access_token
from app.db.schemas import Token, UserLogin

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    user = await get_user_by_email(session, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(user.id), "is_admin": user.is_admin})
    return {"access_token": access_token, "token_type": "bearer"}
