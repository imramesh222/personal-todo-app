from typing import Optional, List
from pydantic import BaseModel, EmailStr
from app.domain.todo import ToDo

class ToDoCreateRequest(BaseModel):
    task: str

class ToDoCreateResponse(BaseModel):
    todo: ToDo

class ToDoUpdateRequest(BaseModel):
    task: Optional[str] = None
    completed: Optional[bool] = None

class ToDoUpdateResponse(BaseModel):
    todo: ToDo

class ToDoListResponse(BaseModel):
    todos: List[ToDo]
    total: int

class ToDoDeleteResponse(BaseModel):
    success: bool
    message: Optional[str] = None
