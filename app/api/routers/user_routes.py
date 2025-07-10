from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.repo.datasource import get_db
from app.utils.auth import get_current_user
from app.domain.user import User
from app.mapper.user_mapper import record_to_user
from app.domain.user_req_res import UserRegisterRequest, UserRegisterResponse, UserUpdateRequest, UserUpdateResponse, UserDeleteResponse
from app.service.user_service import UserService
from app.repo.user_repo import UserRepo
from fastapi import HTTPException, status
from typing import List
from app.model.user_record import UserRecord

user_repo = UserRepo()
user_service = UserService(user_repo)

router = APIRouter(prefix="/users", tags=["Users"])

def require_admin(current_user=Depends(get_current_user)):
    if getattr(current_user, 'role', 'user') != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user

@router.get("/me", response_model=User)
def get_me(current_user = Depends(get_current_user)):
    return record_to_user(current_user)

@router.post("/", response_model=UserRegisterResponse)
def register_user(request: UserRegisterRequest, db: Session = Depends(get_db)):
    user = User(full_name=request.full_name, email=request.email, role=request.role or "user")
    created_user = user_service.register_user(db, user, request.password)
    return UserRegisterResponse(
        id=created_user.id or "",
        full_name=created_user.full_name,
        email=created_user.email,
        role=created_user.role or "user",
        created_at=created_user.created_at,
        updated_at=created_user.updated_at
    )

@router.put("/{user_id}", response_model=UserUpdateResponse)
def update_user(user_id: str, request: UserUpdateRequest, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Admin can update anyone; user can only update themselves
    if current_user.role != "admin" and user_id != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to update this user")
    updates = request.dict(exclude_unset=True)
    updated = user_service.update_user(db, user_id, updates)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserUpdateResponse(
        id=updated.id or "",
        full_name=updated.full_name,
        email=updated.email,
        role=updated.role or "user",
        created_at=updated.created_at,
        updated_at=updated.updated_at
    )

@router.delete("/{user_id}", response_model=UserDeleteResponse)
def delete_user(user_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Admin can delete anyone; user can only delete themselves
    if current_user.role != "admin" and user_id != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to delete this user")
    success = user_service.delete_user(db, user_id)
    if not success:
        return UserDeleteResponse(success=False, message="Not found")
    if user_id == str(current_user.id):
        return UserDeleteResponse(success=True, message="User deleted. Please log out.")
    return UserDeleteResponse(success=True, message="User deleted.")

@router.get("/", response_model=List[User])
def list_users(db: Session = Depends(get_db), current_user=Depends(require_admin)):
    users = db.query(UserRecord).all()
    return [record_to_user(u) for u in users]
