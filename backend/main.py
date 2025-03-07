from os import getenv
from typing import List

from fastapi import FastAPI, Query
from db import DB

from configs import Task, STATUS

app = FastAPI()
db = DB()


@app.get('/')
def test_api():
    return 'Hello world!'


@app.get('/tasks/')
def get_tasks(status_filter: List[int] = Query([]), order: str = 'asc_asc'):
    tasks_return = []
    for task_data in list(db.get_tasks(status_filter, order)):
        tasks_return.append({
            "id": task_data[0],
            "name": task_data[1],
            "description": task_data[2],
            "status": task_data[3],
            "deadline": task_data[4].strftime("%Y-%m-%d %H:%M:%S"),
            "created_by": task_data[5]
        })
    return tasks_return


@app.post('/tasks/')
def create_task(task_data: Task):
    db.create_task(task_data=task_data)


@app.put('/tasks/{task_id}')
def update_task(task_id: int, task_data: Task):
    db.update_task(task_id, task_data)


@app.patch('/tasks/{task_id}')
def change_status(task_id: int, status: int):
    db.change_status(task_id, status)
