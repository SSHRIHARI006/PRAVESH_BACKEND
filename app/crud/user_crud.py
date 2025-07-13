

# create user

from sqlalchemy.orm import Session
from app.db.models import User
from app.db.schemas import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import get_password_hash

async def create_user(session: AsyncSession, user_data: UserCreate):
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        password=hashed_password,
        name=user_data.name,
        phone=user_data.phone,
        gender=user_data.gender,
        bt_id=user_data.bt_id,
        hostel_room_no=user_data.hostel_room_no,
        is_hostel_user=user_data.is_hostel_user,
        is_admin=user_data.is_admin
    )
    session.add(new_user)
    await session.commit()
    return new_user


# fetching user

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_bt_id(db: Session, bt_id: str) -> User | None:
    return db.query(User).filter(User.bt_id == bt_id).first()

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

#update user

def update_user(db: Session, user_id : int,updates : dict) -> User| None :
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        for key, value in updates.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user

# delete user

def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

# verify user

def verify_user_credentials(db: Session, bt_id: str, password: str) -> User | None:
    user = get_user_by_bt_id(db, bt_id)
    if user and user.password == password:
        return user
    return None
