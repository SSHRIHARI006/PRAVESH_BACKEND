

# create user

from sqlalchemy.orm import Session
from app.db.models import User

def create_user(db : Session, user :User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

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
