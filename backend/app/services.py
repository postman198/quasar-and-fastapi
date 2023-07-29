import os as _os
import time

import jwt as _jwt
import sqlalchemy.orm as _orm
from email_validator import validate_email, EmailNotValidError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

import app.database as _database
import app.schemas as _schemas
import app.models as _models

pass_ctx = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"], default="des_crypt")


JWT_SECRET = _os.environ['JWT_SECRET']
ALGORITHM = _os.environ['ALGORITHM']
EXPIRES_IN_SEC = _os.environ['EXPIRES']

oauth2schema = OAuth2PasswordBearer("/token")


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_user_by_email(email: str, db: _orm.Session):
    return db.query(_models.User).filter(_models.User.email == email).first()


async def create_user(user: _schemas.UserCreate, db: _orm.Session):

    try:
        valid = validate_email(email=user.email)

        email = valid.email
    except EmailNotValidError:
        raise HTTPException(status_code=400, detail="Please enter a valid email")

    _user = _models.User(email=email, hashed_password=pass_ctx.hash(user.password))

    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user


async def authenticate_user(email: str, password: str, db: _orm.Session):
    _user = await get_user_by_email(email=email, db=db)

    if not _user:
        return False
    
    if not pass_ctx.verify(password, _user.hashed_password):
        return False

    return _user


async def create_token(user: _models.User):
    _user = _schemas.User.from_orm(user)

    user_dict = _user.model_dump()
    del user_dict["date_created"]
    user_dict["exp"] = time.time() + (int(EXPIRES_IN_SEC)*10)

    token = _jwt.encode(user_dict, JWT_SECRET)

    return dict(access_token=token, token_type="bearer")


async def get_current_user(db: _orm.Session = Depends(get_db), token: str = Depends(oauth2schema)):
    payload = verify_jwt(token)
    if not payload:
        raise HTTPException(status_code=403, detail="Invalid token or expired token.")
    user = db.query(_models.User).get(payload["id"])
    if not user:
        raise HTTPException(status_code=404, detail="user does not exist")
    return user


def verify_jwt(token: str) -> bool:
    try:
        payload = decodeJWT(token)
    except:
        payload = None
    if payload:
        return payload
    return False


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = _jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except:
        return {}


async def create_task(user: _schemas.User, db: _orm.Session, task: _schemas.TaskCreate):
    _task = _models.Task(**task.model_dump(), owner_id=user.id)
    db.add(_task)
    db.commit()
    db.refresh(_task)
    return _schemas.Task.from_orm(_task)


async def get_user_tasks(user: _schemas.User, db: _orm.Session):
    _tasks = db.query(_models.Task).filter_by(owner_id=user.id)

    return list(map(_schemas.Task.from_orm, _tasks))


async def get_user_task_by_id(task_id: int, user: _schemas.User, db: _orm.Session):
    _task = db.query(_models.Task).filter_by(id=task_id,owner_id=user.id).first()
    if not _task:
            raise HTTPException(
                status_code=404, detail=f"Task with task_id = {task_id} not found"
            )
    return _task


async def update_user_task_by_id(task_id: int, task: _schemas.Task, user: _schemas.User, db: _orm.Session):
    _task = await get_user_task_by_id(task_id=task_id, user=user,  db=db)
    if _task.title:
        _task.title = task.title
    if _task.description:
        _task.description = task.description
    if _task.status:
        _task.status = task.status
    db.commit()
    db.refresh(_task)
    return _schemas.Task.from_orm(_task)


async def delete_user_task_by_id(task_id: int, user: _schemas.User, db: _orm.Session):
    _task = await get_user_task_by_id(task_id=task_id, user=user,  db=db)
    db.delete(_task)
    db.commit()
    return _schemas.Task.from_orm(_task)


