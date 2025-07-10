from typing import Optional
from pydantic import BaseModel

class ToDo(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    task: str
    completed: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None 