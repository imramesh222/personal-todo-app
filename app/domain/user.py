from typing import Optional
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: Optional[str] = None
    full_name: str
    email: EmailStr
    password: Optional[str] = None  # Only for input, not output
    role: Optional[str] = "user"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
