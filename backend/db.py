import sqlalchemy as sa
from dotenv import load_dotenv
from os import getenv as env
from configs import Task
load_dotenv()


class DB():
    def __init__(self):
        self.engine = sa.create_engine(
            f"postgresql+psycopg2://{env('PG_USER')}:{env('PG_PASSWORD')}@{env('PG_HOST')}:5432/{env('PG_DATABASE')}")

    def get_tasks(self, status_filter: list, order: str) -> list:
        status_filter_clause = f"WHERE status = ANY(ARRAY{status_filter})" if status_filter else ""

        name_order, deadline_order = order.split('_')
        name_order = name_order.lower() if name_order.lower() in ('asc', 'desc') else 'asc'
        deadline_order = deadline_order.lower(
        ) if deadline_order.lower() in ('asc', 'desc') else 'asc'

        query = f"""
            SELECT * FROM tasks
            {status_filter_clause}
            ORDER BY name {name_order}, deadline {deadline_order}
        """

        with self.engine.connect() as conn:
            res = conn.execute(sa.text(query))
            return res

    def create_task(self, task_data: Task) -> None:
        insert_string = sa.text("""
            INSERT INTO tasks(name, description, status, deadline, created_by)
            VALUES(
                :name,
                :description,
                :status,
                :deadline,
                :created_by
            )
        """)
        with self.engine.connect() as conn:
            conn.execute(insert_string, {
                "name": task_data.name,
                "description": task_data.description,
                "status": task_data.status,
                "deadline": task_data.deadline,
                "created_by": task_data.created_by
            })
            conn.commit()

    def update_task(self, task_id: int, task_data: Task) -> None:
        task_data_dict = dict(task_data)
        del task_data_dict["id"]
        update_string = sa.text(f"""
            UPDATE tasks
            SET {', '.join([f"{column} = :{column}" for column in task_data_dict.keys()])}
            WHERE id = :id
        """)
        params = task_data_dict.copy()
        params['id'] = task_id
        with self.engine.connect() as conn:
            conn.execute(update_string, params)
            conn.commit()

    def change_status(self, task_id: int, status: int) -> None:
        update_string = sa.text("""
            UPDATE tasks
            SET status = :status
            WHERE id = :task_id
        """)
        with self.engine.connect() as conn:
            conn.execute(update_string, {
                "status": status,
                "task_id": task_id
            })
            conn.commit()
