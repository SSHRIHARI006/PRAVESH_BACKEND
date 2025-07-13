from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud.user_crud import verify_user_credentials
from app.auth import jwt, schemas

router = APIRouter()

@router.post("/login", response_model=schemas.Token)
def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = verify_user_credentials(db, request.bt_id, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect BT ID or password",
        )
    access_token = jwt.create_access_token(data={"sub": user.bt_id})
    return {"access_token": access_token, "token_type": "bearer"}
