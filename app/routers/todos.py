from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Todo
from ..schemas import TodoCreate, TodoRead, TodoUpdate


router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate, db_session: Session = Depends(get_db)) -> Todo:
    todo = Todo(
        title=payload.title,
        description=payload.description,
        completed=payload.completed or False,
    )
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)
    return todo


@router.get("", response_model=List[TodoRead])
def list_todos(
    db_session: Session = Depends(get_db),
    *,
    search: Optional[str] = Query(default=None, description="Search by title"),
    completed: Optional[bool] = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
):
    statement = select(Todo)

    if search:
        statement = statement.where(Todo.title.ilike(f"%{search}%"))
    if completed is not None:
        statement = statement.where(Todo.completed.is_(completed))

    statement = statement.order_by(Todo.created_at.desc()).offset(skip).limit(limit)
    return list(db_session.execute(statement).scalars().all())


@router.get("/{todo_id}", response_model=TodoRead)
def get_todo(todo_id: int, db_session: Session = Depends(get_db)) -> Todo:
    todo = db_session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=TodoRead)
def update_todo(
    todo_id: int,
    payload: TodoUpdate,
    db_session: Session = Depends(get_db),
):
    todo = db_session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(todo, key, value)
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)
    return todo


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_todo(todo_id: int, db_session: Session = Depends(get_db)) -> Response:
    todo = db_session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    db_session.delete(todo)
    db_session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{todo_id}/toggle", response_model=TodoRead)
def toggle_todo(todo_id: int, db_session: Session = Depends(get_db)) -> Todo:
    todo = db_session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    todo.completed = not todo.completed
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)
    return todo

