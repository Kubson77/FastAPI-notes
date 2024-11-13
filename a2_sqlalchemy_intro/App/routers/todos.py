from typing import Annotated

from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException, Path
from models import Todos
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

router = APIRouter()


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# The parameter `db: Annotated[Session, Depends(get_db)]` does the following:
# - `db` is annotated with `Session` (an SQLAlchemy session) and `Depends(get_db)`.
# - `Depends(get_db)` tells FastAPI to call the `get_db()` function to retrieve
#   a database session for each request.
# - `get_db()` yields a session, ensuring a new session is opened for each request,
#   and closes it automatically after the request completes, to prevent open connections.
#
# The function `read_all` then uses this session (`db`) to query the Todos table,
# calling `db.query(Todos).all()` to retrieve all records.
# FastAPI converts the query result to JSON and returns it as the response.
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(
    db: Annotated[Session, Depends(get_db)],
):
    return db.query(Todos).all()


# To avoid duplicating the dependency annotation for database sessions in each route,
# we extract the `db: Annotated[Session, Depends(get_db)]` parameter into a global
# variable, `db_dependency`. This variable can then be reused wherever the database
# dependency is needed, promoting consistency and simplifying updates to dependency definitions.
db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found.")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.model_dump())

    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0),
):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    db.query(Todos).filter(Todos.id == todo_id).delete()

    db.commit()
