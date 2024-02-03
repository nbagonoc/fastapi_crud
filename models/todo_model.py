from sqlalchemy import Boolean, Column, Integer, String
from db import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), index=True)