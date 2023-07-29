from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas import User, Task, TaskCreate
import app.services as _services

task_router = APIRouter()


@task_router.post("/create")
async def create_task(
    task: TaskCreate,
    user: User = Depends(_services.get_current_user),
    db: Session = Depends(_services.get_db)
):
    await _services.create_task(user=user, db=db, task=task)
    return "Task created successfully"


@task_router.get("/current-user-tasks", response_model=List[Task])
async def get_user_tasks(user: User = Depends(_services.get_current_user),
                         db: Session = Depends(_services.get_db)):
    return await _services.get_user_tasks(user=user, db=db)


@task_router.get("/{task_id}", response_model=Task)
async def get_user_task_by_id(task_id: int, user: User = Depends(_services.get_current_user),
                         db: Session = Depends(_services.get_db)):
    _task = await _services.get_user_task_by_id(task_id=task_id, user=user,  db=db)
    return Task.from_orm(_task)

@task_router.patch("/{task_id}", response_model=Task)
async def update_user_task_by_id(task_id: int, task: TaskCreate, user: User = Depends(_services.get_current_user),
                         db: Session = Depends(_services.get_db)):
    return await _services.update_user_task_by_id(task_id=task_id, task=task, user=user,  db=db)


@task_router.delete("/{task_id}")
async def delete_user_task_by_id(task_id: int, user: User = Depends(_services.get_current_user),
                         db: Session = Depends(_services.get_db)):
    await _services.delete_user_task_by_id(task_id=task_id, user=user,  db=db)
    return "Task deleted successfully"
