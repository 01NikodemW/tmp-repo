import os
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Path, Request, Response

from .database import connect, initialize
from .repository import TodoRepository
from .schemas import Todo, TodoCreate, TodoUpdate


def repository(request: Request):
    connection = connect(request.app.state.database_path)
    try:
        yield TodoRepository(connection)
    finally:
        connection.close()


Repository = Annotated[TodoRepository, Depends(repository)]
TodoId = Annotated[int, Path(gt=0)]


def create_app(database_path: str | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        initialize(app.state.database_path)
        yield

    app = FastAPI(title="Taskly API", version="1.0.0", lifespan=lifespan)
    app.state.database_path = database_path or os.getenv("DATABASE_PATH", "data/todos.db")

    @app.get("/api/health", tags=["health"])
    def health(repo: Repository):
        repo.connection.execute("SELECT 1 FROM todos LIMIT 1")
        return {"status": "ok"}

    @app.get("/api/todos", response_model=list[Todo], tags=["todos"])
    def list_todos(repo: Repository):
        return repo.list()

    @app.post("/api/todos", response_model=Todo, status_code=201, tags=["todos"])
    def create_todo(payload: TodoCreate, repo: Repository):
        return repo.create(payload)

    @app.get("/api/todos/{todo_id}", response_model=Todo, tags=["todos"])
    def get_todo(todo_id: TodoId, repo: Repository):
        todo = repo.get(todo_id)
        if todo is None:
            raise HTTPException(404, "Task not found.")
        return todo

    @app.patch("/api/todos/{todo_id}", response_model=Todo, tags=["todos"])
    def update_todo(todo_id: TodoId, payload: TodoUpdate, repo: Repository):
        todo = repo.update(todo_id, payload)
        if todo is None:
            raise HTTPException(404, "Task not found.")
        return todo

    @app.delete("/api/todos/{todo_id}", status_code=204, tags=["todos"])
    def delete_todo(todo_id: TodoId, repo: Repository):
        if not repo.delete(todo_id):
            raise HTTPException(404, "Task not found.")
        return Response(status_code=204)

    return app


app = create_app()
