from fastapi import FastAPI
from models import Todo

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

todos = []

#get all todos
@app.get("/todos")
async def get_todos():
    return {"todos": todos}

#get single todo
@app.get("/todos/{id}")
async def get_single_todo(id: int):
    for todo in todos:
        if todo.id == id:
            return {"todo": todo}
    return {"message": "Todo not found"}

#create todo
@app.post("/todos")
async def create_todos(todo: Todo):
    todos.append(todo)
    return {"message": "Todo has been created successfully"}


#update todo
@app.put("/todos/{id}")
async def update_todos(id: int, todo: Todo):
    for t in todos:
        if t.id == id:
            t.title = todo.title
            return {"message": "Todo has been updated successfully"}
    return {"message": "Todo not found"}

#delete todo
@app.delete("/todos/{id}")
async def delete_todos(id: int):
    for todo in todos:
        if todo.id == id:
            todos.remove(todo)
            return {"message": "Todo has been deleted successfully"}
    return {"message": "Todo not found"}