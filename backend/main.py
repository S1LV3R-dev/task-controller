from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, Field

class Task(BaseModel):
    id: int
    name: str
    description: str
    status: int
    deadline: datetime

app = FastAPI()

@app.get('/')
def test_api():
    return 'Hello world!'

@app.post('/tasks/')
def create_task(task_data: Task):
    print(task_data)