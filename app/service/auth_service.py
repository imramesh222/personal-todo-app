from app.repo.user_repo import UserRepo
from app.utils.hashing import Hash
from app.utils.auth import create_access_token
from sqlalchemy.orm import Session

class AuthService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    def authenticate_user(self, db: Session, email: str, password: str):
        user_record = self.user_repo.get_by_email(db, email)
        if not user_record:
            return None
        if not Hash.verify(password, user_record.password):
            return None
        return user_record

    def create_access_token(self, user_id: str):
        return create_access_token({"sub": user_id})
