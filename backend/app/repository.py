import sqlite3
from datetime import datetime, timezone

from .schemas import Todo, TodoCreate, TodoUpdate


def from_row(row: sqlite3.Row) -> Todo:
    values = dict(row)
    values["completed"] = bool(values["completed"])
    return Todo.model_validate(values)


class TodoRepository:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def list(self) -> list[Todo]:
        rows = self.connection.execute("SELECT * FROM todos ORDER BY created_at DESC, id DESC")
        return [from_row(row) for row in rows]

    def get(self, todo_id: int) -> Todo | None:
        row = self.connection.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
        return from_row(row) if row else None

    def create(self, payload: TodoCreate) -> Todo:
        now = datetime.now(timezone.utc).isoformat()
        values = payload.model_dump(mode="json")
        with self.connection:
            cursor = self.connection.execute(
                """INSERT INTO todos
                (title, description, priority, due_date, completed, created_at, updated_at)
                VALUES (:title, :description, :priority, :due_date, :completed, :created_at, :updated_at)""",
                {**values, "created_at": now, "updated_at": now},
            )
        return self.get(cursor.lastrowid)

    def update(self, todo_id: int, payload: TodoUpdate) -> Todo | None:
        values = payload.model_dump(mode="json", exclude_unset=True)
        values["updated_at"] = datetime.now(timezone.utc).isoformat()
        # Column names come exclusively from the validated Pydantic schema.
        assignments = ", ".join(f"{key} = ?" for key in values)
        with self.connection:
            cursor = self.connection.execute(
                f"UPDATE todos SET {assignments} WHERE id = ?", (*values.values(), todo_id)
            )
        return self.get(todo_id) if cursor.rowcount else None

    def delete(self, todo_id: int) -> bool:
        with self.connection:
            cursor = self.connection.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        return cursor.rowcount > 0
