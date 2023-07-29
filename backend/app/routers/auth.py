from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

import app.services as _services

auth_router = APIRouter()


@auth_router.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(_services.get_db)):
    user = await _services.authenticate_user(email=form_data.username, password=form_data.password, db=db)

    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid Credentials")

    return await _services.create_token(user=user)


