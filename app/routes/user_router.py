from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from core.database import get_db
from app.schemas.user import UserSchema, UserCreate, UserAuth
from app.services.user_service import create_user, authenticate_user, generate_token

user_router = APIRouter()


@user_router.post("/register", response_model=UserSchema)
def user_post(user: UserCreate, db:Session = Depends(get_db)):
    return create_user(db, user)


@user_router.post("/login")
def login_for_access_token(user: UserAuth, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.username, user.password)
    access_token = generate_token(db_user)
    return {"access_token": access_token, "token_type": "bearer"}
