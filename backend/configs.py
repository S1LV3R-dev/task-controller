from datetime import datetime
from pydantic import BaseModel
from os import getenv as env
from dotenv import load_dotenv

load_dotenv()

class STATUS():
    NEW = 0
    IN_PROGRESS = 1
    DONE = 2
    CANCELED = -1

class Task(BaseModel):
    id: int = None
    name: str
    description: str
    deadline: datetime
    status: int = STATUS.NEW
    created_by: int = 0

JWT_SECRET_KEY = str(env("JWT_SECRET_KEY"))