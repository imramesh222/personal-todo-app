# app/domain/auth_req_res.py
from pydantic import BaseModel, EmailStr

class AuthLoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"