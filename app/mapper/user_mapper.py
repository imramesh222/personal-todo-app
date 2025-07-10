from app.domain.user import User
from app.model.user_record import UserRecord

__all__ = ["record_to_user", "user_to_record"]

def user_to_record(user: User, hashed_password: str = None) -> UserRecord:
    kwargs = {
        'full_name': user.full_name,
        'email': user.email,
        'password': hashed_password if hashed_password else "",
        'role': user.role if hasattr(user, 'role') and user.role else "user"
    }
    if user.id:
        kwargs['id'] = str(user.id)
    return UserRecord(**kwargs)

def user_update_to_record(user: User, updates: dict) -> UserRecord:
    # Only update provided fields
    data = user.dict()
    data.update({k: v for k, v in updates.items() if v is not None})
    return user_to_record(User(**data), data.get('password'))

def record_to_user(record: UserRecord) -> User:
    user_data = {
        'full_name': getattr(record, 'full_name', '') or '',
        'email': getattr(record, 'email', '') or '',
        'role': getattr(record, 'role', 'user')
    }
    if getattr(record, 'id', None):
        user_data['id'] = str(getattr(record, 'id'))
    if getattr(record, 'created_at', None):
        user_data['created_at'] = getattr(record, 'created_at').isoformat()
    if getattr(record, 'updated_at', None):
        user_data['updated_at'] = getattr(record, 'updated_at').isoformat()
    return User(**user_data)
