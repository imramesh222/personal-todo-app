from typing import Optional
from pydantic import BaseModel, EmailStr
from app.domain.user import User

class UserRegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"

class UserRegisterResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    role: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserUpdateResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    role: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class UserDeleteResponse(BaseModel):
    success: bool
    message: Optional[str] = None
