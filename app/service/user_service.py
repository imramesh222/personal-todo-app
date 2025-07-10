from app.repo.user_repo import UserRepo
from app.domain.user import User
from app.utils.hashing import Hash
from sqlalchemy.orm import Session
from typing import Optional

class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    def register_user(self, db: Session, user: User, password: str) -> User:
        hashed_password = Hash.hash(password)
        return self.user_repo.create(db, user, hashed_password)

    def get_user_by_id(self, db: Session, user_id: str) -> Optional[User]:
        user_record = self.user_repo.get_by_id(db, user_id)
        if not user_record:
            return None
        return user_record

    def update_user(self, db: Session, user_id: str, updates: dict):
        return self.user_repo.update(db, user_id, updates)

    def delete_user(self, db: Session, user_id: str) -> bool:
        return self.user_repo.delete(db, user_id)
