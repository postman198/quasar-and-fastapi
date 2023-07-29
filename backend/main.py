import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers.auth import auth_router
from app.routers.user import user_router
from app.routers.task import task_router

Base.metadata.create_all(engine)

app = FastAPI()

origins = [
    "http://localhost:8080",
    # more origins here if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router, prefix="/api/users", tags=["user"])
app.include_router(task_router, prefix="/api/tasks", tags=["task"])


# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8005)
