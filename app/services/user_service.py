from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.models import User
from app.schemas.user import UserCreate, UserAuth, Token
from app.services.auth import create_access_token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(
        name=user.name,
        username=user.username,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, username: str, password: str):
    db_user = get_user_by_username(db, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if not pwd_context.verify(password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return db_user


def generate_token(db_user: UserAuth) -> Token:
    return create_access_token(data={"sub": db_user.username})
