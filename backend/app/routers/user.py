from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import User, UserCreate
import app.services as _services

user_router = APIRouter()


@user_router.post("/signup")
async def create_user(user: UserCreate, db: Session = Depends(_services.get_db)):
    db_user = await _services.get_user_by_email(email=user.email, db=db)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="User with that email already exists")

    await _services.create_user(user=user, db=db)
    return "User created successfully"


@user_router.get("/current-user", response_model=User)
async def get_user(user: User = Depends(_services.get_current_user)):
    return user

