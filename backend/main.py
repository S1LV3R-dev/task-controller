from os import getenv
from typing import List

from fastapi import FastAPI, Query
from db import DB

from configs import Task, STATUS

app = FastAPI()
db = DB()


@app.get('/tasks/')
def get_tasks(status_filter: List[int] = Query([]), order: str = 'asc_asc'):
    return db.get_tasks(status_filter, order)


@app.get('/tasks/{task_id}')
def get_tasks(task_id: int):
    return db.get_task_by_id(task_id=task_id)


@app.post('/tasks/')
def create_task(task_data: Task):
    db.create_task(task_data=task_data)


@app.put('/tasks/{task_id}')
def update_task(task_id: int, task_data: Task):
    db.update_task(task_id, task_data)


@app.patch('/tasks/{task_id}')
def change_status(task_id: int, status: int):
    db.change_status(task_id, status)
