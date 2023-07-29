import datetime as _dt
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "abc@abc.com",
                "password": "any"
            }
        }


class User(UserBase):
    id: Optional[int] = None
    date_created: _dt.datetime

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = 'Open'

    class Config:
        json_schema_extra = {
            "example": {
                "title": "any title",
                "description": "description for the title...",
                "status": "Open/Done"
            }
        }


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: Optional[int] = None
    owner_id: Optional[int] = None
    date_created: _dt.datetime

    class Config:
        from_attributes = True
