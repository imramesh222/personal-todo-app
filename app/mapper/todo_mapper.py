from app.domain.todo import ToDo
from app.model.todo_record import ToDoRecord

def todo_to_record(todo: ToDo) -> ToDoRecord:
    return ToDoRecord(
        id=str(todo.id),
        user_id=str(todo.user_id),
        task=todo.task,
        completed=todo.completed
    )

def record_to_todo(record: ToDoRecord) -> ToDo:
    return ToDo(
        id=str(getattr(record, 'id', None)),
        user_id=str(getattr(record, 'user_id', None)),
        task=getattr(record, 'task', ''),
        completed=getattr(record, 'completed', False),
        created_at=getattr(record, 'created_at', None).isoformat() if getattr(record, 'created_at', None) else None,
        updated_at=getattr(record, 'updated_at', None).isoformat() if getattr(record, 'updated_at', None) else None
    )
