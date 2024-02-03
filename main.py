from fastapi import FastAPI
from db import engine, Base

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Include the router
from routes.todo_route import router as todo_router
app.include_router(todo_router, prefix="/api/v1/todos")
