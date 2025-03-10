import sqlalchemy as sa
from dotenv import load_dotenv
from os import getenv as env
from configs import Task
load_dotenv()


class DB():
    def __init__(self):
        self.engine = sa.create_engine(
            f"postgresql+psycopg2://{env('PG_USER')}:{env('PG_PASSWORD')}@{env('PG_HOST')}:5432/{env('PG_DATABASE')}")

    def execute_query(self, query: str, params: dict = {}, commit: bool = False):
        with self.engine.connect() as conn:
            res = conn.execute(sa.text(query), parameters=params)
            if commit:
                conn.commit()
            try:
                return [dict(row._mapping) for row in res.fetchall()]
            except:
                return None

    def get_task_by_id(self, task_id: int) -> Task:
        query = f"""
            SELECT * FROM tasks
            WHERE id = :id
        """
        try:
            return Task(**self.execute_query(query=query, params={"id": task_id})[0])
        except IndexError:
            return 404

    def get_tasks(self) -> list:

        query = f"""
            SELECT tasks.id, tasks.name, tasks.description, tasks.status, tasks.deadline, users.username FROM tasks
            JOIN users ON tasks.created_by = users.id
        """
        return self.execute_query(query=query)

    def create_task(self, task_data: Task, creator: int) -> None:
        query = """
            INSERT INTO tasks(name, description, status, deadline, created_by)
            VALUES(
                :name,
                :description,
                :status,
                :deadline,
                :created_by
            )
            RETURNING *
        """
        return self.execute_query(query, {
            "name": task_data.name,
            "description": task_data.description,
            "status": task_data.status,
            "deadline": task_data.deadline,
            "created_by": creator
        }, commit=True)

    def update_task(self, task_id: int, task_data: Task) -> None:
        task_data_dict = dict(task_data)
        del task_data_dict["id"]
        query = f"""
            UPDATE tasks
            SET {', '.join([f"{column} = :{column}" for column in task_data_dict.keys()])}
            WHERE id = :id
        """
        params = task_data_dict.copy()
        params['id'] = task_id
        return self.execute_query(query=query, params=params, commit=True)

    def change_status(self, task_id: int, status: int) -> None:
        query = """
            UPDATE tasks
            SET status = :status
            WHERE id = :task_id
        """
        return self.execute_query(query, {
            "status": status,
            "task_id": task_id
        }, commit=True)

    def login(self, login_str: str, password_hash: str):
        query = """
            SELECT * FROM users
            WHERE username = :login_str
            OR
            email = :login_str
        """
        res = self.execute_query(query=query, params={"login_str": login_str})
        if not res or res[0]['password'] != password_hash:
            return False
        else:
            return res[0]

    def register(self, username: str, email: str, password_hash: str):
        query = """
            SELECT * FROM users
            WHERE 
            email = :email
        """
        res = self.execute_query(query=query, params={
            "email": email
        })
        if res:
            return False
        query = """
            INSERT INTO users(username, email, password)
            VALUES(
                :username,
                :email,
                :password
            )
            ON CONFLICT DO NOTHING
        """
        self.execute_query(query=query, params={
            "username": username,
            "email": email,
            "password": password_hash
        }, commit=True)
        query = """
            SELECT * FROM users
            WHERE 
            email = :email
        """
        res = self.execute_query(query=query, params={
            "email": email
        })
        return res[0]

    def delete_task(self, task_id: int) -> None:
        query = f"""
            DELETE FROM tasks
            WHERE id = :id
        """
        return self.execute_query(query=query, params={"id": task_id}, commit=True)