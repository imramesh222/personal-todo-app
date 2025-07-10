from sqlalchemy.orm import Session
from app.model.user_record import UserRecord
from app.domain.user import User
from app.mapper.user_mapper import record_to_user, user_to_record
from app.utils.hashing import Hash
import uuid

class UserRepo:
    def get_by_email(self, db: Session, email: str):
        return db.query(UserRecord).filter(UserRecord.email == email).first()

    def get_by_id(self, db: Session, user_id: str):
        return db.query(UserRecord).filter(UserRecord.id == user_id).first()

    def create(self, db: Session, user: User, hashed_password: str):
        user_id = str(uuid.uuid4())
        user_record = user_to_record(User(id=user_id, full_name=user.full_name, email=user.email, role=user.role), hashed_password)
        db.add(user_record)
        db.commit()
        db.refresh(user_record)
        return record_to_user(user_record)

    def update(self, db: Session, user_id: str, updates: dict):
        user_record = self.get_by_id(db, user_id)
        if not user_record:
            return None
        for key, value in updates.items():
            if value is not None and hasattr(user_record, key):
                # Hash the password if it's being updated
                if key == "password":
                    value = Hash.hash(value)
                setattr(user_record, key, value)
        db.commit()
        db.refresh(user_record)
        return record_to_user(user_record)

    def delete(self, db: Session, user_id: str) -> bool:
        user_record = self.get_by_id(db, user_id)
        if not user_record:
            return False
        db.delete(user_record)
        db.commit()
        return True

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return Hash.verify(plain_password, hashed_password)
