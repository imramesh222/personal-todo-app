from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.repo.datasource import get_db
from app.domain.auth_req_res import AuthLoginRequest, AuthLoginResponse
from app.domain.user_req_res import UserRegisterRequest, UserRegisterResponse
from app.domain.user import User
from app.service.auth_service import AuthService
from app.service.user_service import UserService
from app.repo.user_repo import UserRepo
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])

user_repo = UserRepo()
auth_service = AuthService(user_repo)
user_service = UserService(user_repo)

@router.post("/login", response_model=AuthLoginResponse)
def login(request: AuthLoginRequest, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, request.email, request.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = auth_service.create_access_token(user.id)
    return AuthLoginResponse(access_token=access_token)

@router.post("/register", response_model=UserRegisterResponse)
def register(request: UserRegisterRequest, db: Session = Depends(get_db)):
    user = User(full_name=request.full_name, email=request.email)
    created_user = user_service.register_user(db, user, request.password)
    return UserRegisterResponse(
        id=created_user.id,
        full_name=created_user.full_name,
        email=created_user.email,
        created_at=created_user.created_at,
        updated_at=created_user.updated_at
    )

@router.post("/token", response_model=AuthLoginResponse)
def login_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = auth_service.create_access_token(user.id)
    return AuthLoginResponse(access_token=access_token)
