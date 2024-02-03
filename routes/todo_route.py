from fastapi import APIRouter, HTTPException, status, Depends
from db import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from schemas.todo_schema import TodoSchema
from models.todo_model import Todo

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

#get all todos
@router.get("/", status_code=status.HTTP_200_OK)
async def get_todos(db: db_dependency):
    todos = db.query(Todo).all()
    return {"todos": todos}


#get single todo
@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_single_todo(id: int, db: db_dependency):
    todo = db.query(Todo).filter(Todo.id == id).first()

    if todo:
        return todo
    else:
        raise HTTPException(status_code=404, detail="Todo not found")

#create todo
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todos(todo: TodoSchema, db: db_dependency):
    todo = Todo(**todo.model_dump())
    db.add(todo)
    db.commit()
    return {"message": "Todo has been created successfully"}

#update todo
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_todos(id: int, todo: TodoSchema, db: Session = Depends(get_db)):
    existing_todo = db.query(Todo).filter(Todo.id == id).first()

    if existing_todo:
        for field, value in todo.model_dump().items():
            setattr(existing_todo, field, value)

        db.commit()
        db.refresh(existing_todo)

        return {"message": "Todo updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Todo not found")

#delete todo
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_todos(id: int, db: db_dependency):
    todo = db.query(Todo).filter(Todo.id == id).first()
    if todo:
        db.delete(todo)
        db.commit()
        return {"message": "Todo deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Todo not found")