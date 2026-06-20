from fastapi import FastAPI;
from src.utils.db import Base, engine
from src.tasks.models import TaskModel
from src.tasks.router import task_router
from src.users.router import user_router


Base.metadata.create_all(engine) # when server will start this go and try to connect BD first

app = FastAPI(title="Task Management Application", description="This is my first project in FastAPI")

app.include_router(task_router)
app.include_router(user_router)