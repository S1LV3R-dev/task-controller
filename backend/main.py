from typing import List
from hashlib import md5
from datetime import datetime, timedelta
import json
import logging
import os

from fastapi import FastAPI, Query, Body, Request, status, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from db import DB
import jwt

from configs import Task, JWT_SECRET_KEY


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()
app = FastAPI()
db = DB()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_filename = datetime.now().strftime("%d-%m-%Y.log")
log_filepath = os.path.join(LOG_DIR, log_filename)
logging.basicConfig(
    filename=log_filepath,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logging.info("Server started")

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
                            httponly=True, max_age=4000)
    return response


@app.middleware("http")
async def check_cookie_middleware(request: Request, call_next):
    CORS_headers = {
            "Access-Control-Allow-Origin": request.headers.get("Origin", "*"),
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS,PATCH",
            "Access-Control-Allow-Headers": request.headers.get("Access-Control-Request-Headers", "*"),
            "Access-Control-Allow-Credentials": "true",
        }
    if request.method == "OPTIONS":
        return Response(status_code=200, headers=CORS_headers)

    renew = None

    if request.url.path not in ["/register", "/login", "/"]:
        token_str = request.cookies.get("token")
        if not token_str:
            return JSONResponse(
                {"detail": "Not authenticated"},
                status_code=status.HTTP_403_FORBIDDEN,
                headers=CORS_headers
            )
        else:
            user_id, token = token_str.split(":")
            try:
                jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                response = JSONResponse(
                    {"details": "Token expired"},
                    status_code=status.HTTP_200_OK,
                    headers=CORS_headers
                )
                renew = True
            except jwt.InvalidTokenError:
                return JSONResponse(
                    {"detail": "Invalid token."},
                    status_code=status.HTTP_403_FORBIDDEN,
                    headers=CORS_headers
                )

    response = await call_next(request)
    if renew:
        response.set_cookie(key='token', value=gen_token(user_id),
                            httponly=True, max_age=4000)
    return response

@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    logging.info(f"{request.method} {request.url.path} - {response.status_code}")
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

@app.websocket("/ws/tasks")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get('/tasks')
def get_tasks():
    return db.get_tasks()


@app.get('/tasks/{task_id}')
def get_tasks(task_id: int):
    task = db.get_task_by_id(task_id=task_id)
    if task == 404:
        return JSONResponse({"details": "Task doesn't found"}, status_code=status.HTTP_404_NOT_FOUND)
    else:
        return task


@app.post('/tasks')
def create_task(request: Request, task_data: Task):
    user_id, _ = request.cookies.get("token").split(":")
    task = db.create_task(task_data=task_data, creator=user_id)
    return JSONResponse([{key: str(value) for key, value in task[0].items()}], status_code=status.HTTP_200_OK)

@app.put('/tasks/{task_id}')
def update_task(task_id: int, task_data: Task):
    db.update_task(task_id, task_data)

@app.patch('/tasks/{task_id}')
async def change_status(task_id: int, status: str):
    db.change_status(task_id, int(status))
    message = json.dumps({
        "task_id": task_id,
        "status": int(status)
    })
    return await manager.broadcast(message)

@app.delete('/tasks/{task_id}')
def update_task(task_id: int):
    db.delete_task(task_id)

@app.post('/logout')
def logout(response: Response):
    response.delete_cookie("token")
    return {"detail": "Logout successful"}