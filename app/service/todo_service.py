from app.repo.todo_repo import ToDoRepo
from app.domain.todo import ToDo
from sqlalchemy.orm import Session

class ToDoService:
    def __init__(self, todo_repo: ToDoRepo):
        self.todo_repo = todo_repo

    def create_todo(self, db: Session, todo: ToDo) -> ToDo:
        return self.todo_repo.create(db, todo)

    def get_todo_by_id(self, db: Session, todo_id: str) -> ToDo:
        record = self.todo_repo.get_by_id(db, todo_id)
        if not record:
            return None
        from app.mapper.todo_mapper import record_to_todo
        return record_to_todo(record)

    def list_todos_by_user(self, db: Session, user_id: str, skip: int = 0, limit: int = 10):
        records = self.todo_repo.list_by_user(db, user_id, skip, limit)
        from app.mapper.todo_mapper import record_to_todo
        return [record_to_todo(r) for r in records]

    def list_all_todos(self, db: Session, skip: int = 0, limit: int = 10):
        records = self.todo_repo.list_all(db, skip, limit)
        from app.mapper.todo_mapper import record_to_todo
        return [record_to_todo(r) for r in records]

    def update_todo(self, db: Session, todo_id: str, updates: dict) -> ToDo:
        return self.todo_repo.update(db, todo_id, updates)

    def delete_todo(self, db: Session, todo_id: str) -> bool:
        return self.todo_repo.delete(db, todo_id)
