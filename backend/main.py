from typing import List
from hashlib import md5
from datetime import datetime, timedelta

from fastapi import FastAPI, Query, Response, Body, Request, status
from fastapi.responses import JSONResponse
from db import DB
import jwt

from configs import Task, JWT_SECRET_KEY

app = FastAPI()
db = DB()


def gen_token(user_id: int) -> str:
    return f"""{user_id}:{str(jwt.encode({
        'user_id': user_id,
        'exp': datetime.now()+timedelta(hours=1)
    }, JWT_SECRET_KEY, algorithm="HS256"))}"""


def password_encode(password: str) -> str:
    return md5(password.encode()).hexdigest()


def gen_response_with_token(user_data, error_string):
    token = None
    details = None
    if user_data:
        status_code = 200
        token = gen_token(user_data['id'])
    else:
        details = error_string
        status_code = -1
    response = JSONResponse(
        {"details": details},
        status_code=status_code
    )
    if token:
        response.set_cookie(key='token', value=token,
                            httponly=True, max_age=3600)
    return response


@app.middleware("http")
async def check_cookie_middleware(request: Request, call_next):
    renew = None
    if request.url.path not in ["/register", "/login", "/"]:
        token_str = request.cookies.get("token")
        if not token_str:
            return JSONResponse(
                {"detail": "Not authenticated"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        else:
            user_id, token = token_str.split(":")
            try:
                jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                response = JSONResponse(
                    {"details": ""},
                    status_code=status.HTTP_200_OK
                )
            except jwt.InvalidTokenError:
                return JSONResponse(
                    {"detail": "Invalid token."},
                    status_code=status.HTTP_403_FORBIDDEN
                )

    response = await call_next(request)
    if renew:
        response.set_cookie(key='token', value=gen_token(user_id),
                            httponly=True, max_age=3600)
    return response


@app.post('/register')
def register(
    username: str = Body(...),
    email: str = Body(...),
    password: str = Body(...)
):
    res = db.register(username, email, password_encode(password))
    response = gen_response_with_token(res, "Email already in use")
    if response.status_code != status.HTTP_200_OK:
        response.status_code = status.HTTP_409_CONFLICT
    return response


@app.post('/login')
def login(
    login_str: str = Body(...),
    password: str = Body(...)
):
    res = db.login(login_str, password_encode(password))
    response = gen_response_with_token(res, "Invalid credentials")
    if response.status_code != status.HTTP_200_OK:
        response.status_code = status.HTTP_401_UNAUTHORIZED
    return response


@app.get('/tasks')
def get_tasks(status_filter: List[int] = Query([]), order: str = 'asc_asc'):
    return db.get_tasks(status_filter, order)


@app.get('/tasks/{task_id}')
def get_tasks(task_id: int):
    return db.get_task_by_id(task_id=task_id)


@app.post('/tasks')
def create_task(task_data: Task):
    db.create_task(task_data=task_data)


@app.put('/tasks/{task_id}')
def update_task(task_id: int, task_data: Task):
    db.update_task(task_id, task_data)


@app.patch('/tasks/{task_id}')
def change_status(task_id: int, status: int):
    db.change_status(task_id, status)
