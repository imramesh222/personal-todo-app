from sqlalchemy.orm import Session
from app.model.todo_record import ToDoRecord
from app.domain.todo import ToDo
from app.mapper.todo_mapper import record_to_todo, todo_to_record
import uuid

class ToDoRepo:
    def create(self, db: Session, todo: ToDo) -> ToDo:
        todo_id = str(uuid.uuid4())
        todo_record = todo_to_record(ToDo(id=todo_id, user_id=todo.user_id, task=todo.task, completed=todo.completed))
        db.add(todo_record)
        db.commit()
        db.refresh(todo_record)
        return record_to_todo(todo_record)

    def get_by_id(self, db: Session, todo_id: str) -> ToDoRecord:
        return db.query(ToDoRecord).filter(ToDoRecord.id == todo_id).first()

    def list_by_user(self, db: Session, user_id: str, skip: int = 0, limit: int = 10):
        return db.query(ToDoRecord).filter(ToDoRecord.user_id == user_id).offset(skip).limit(limit).all()

    def list_all(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(ToDoRecord).offset(skip).limit(limit).all()

    def update(self, db: Session, todo_id: str, updates: dict) -> ToDo:
        todo_record = self.get_by_id(db, todo_id)
        if not todo_record:
            return None
        for key, value in updates.items():
            setattr(todo_record, key, value)
        db.commit()
        db.refresh(todo_record)
        return record_to_todo(todo_record)

    def delete(self, db: Session, todo_id: str) -> bool:
        todo_record = self.get_by_id(db, todo_id)
        if not todo_record:
            return False
        db.delete(todo_record)
        db.commit()
        return True
