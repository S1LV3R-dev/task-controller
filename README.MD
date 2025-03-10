# Task controller

## Local deployment
### Backend
1. Navigate to backend folder
```sh
cd backend
```
2. Create virtual environment using venv
```sh
python -m venv .venv
```
3. Activate virtual environment
    Unix
    ```sh
    source .venv/bin/activate
    ```
    Windows
    ```sh
    .venv\Scripts\activate.bat
    ```
4. Install required python packages
```sh
pip install -r requirements.txt
```
5. Make migrations using alembic
```sh
alembic upgrade head
```
6. Run backend using fastapi
```sh
fastapi dev main.py
```
### Frontend
1. Navigate to frontend folder
```sh
cd frontend
```
2. Install required npm packages
```sh
npm i
```
3. Run frontend 
```sh
npm run dev
```
## Docker

Debug
```sh
docker-compose up --build
```

Detached mode
```sh
docker-compose up --build -d
```