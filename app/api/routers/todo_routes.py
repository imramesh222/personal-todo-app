from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.repo.datasource import get_db
from app.utils.auth import get_current_user
from app.domain.todo import ToDo
from app.domain.todo_req_res import ToDoCreateRequest, ToDoCreateResponse, ToDoUpdateRequest, ToDoUpdateResponse, ToDoListResponse, ToDoDeleteResponse
from app.service.todo_service import ToDoService
from app.repo.todo_repo import ToDoRepo

router = APIRouter(prefix="/todos", tags=["ToDos"])

todo_repo = ToDoRepo()
todo_service = ToDoService(todo_repo)

@router.get("/", response_model=ToDoListResponse)
def list_todos(skip: int = Query(0), limit: int = Query(10), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if getattr(current_user, 'role', 'user') == 'admin':
        todos = todo_service.list_all_todos(db, skip, limit)
    else:
        todos = todo_service.list_todos_by_user(db, current_user.id, skip, limit)
    return ToDoListResponse(todos=todos, total=len(todos))

@router.post("/", response_model=ToDoCreateResponse)
def create_todo(request: ToDoCreateRequest, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    todo = ToDo(
        user_id=current_user.id,
        task=request.task,
        completed=False
    )
    created = todo_service.create_todo(db, todo)
    return ToDoCreateResponse(todo=created)

@router.put("/{todo_id}", response_model=ToDoUpdateResponse)
def update_todo(todo_id: str, request: ToDoUpdateRequest, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    todo = todo_service.get_todo_by_id(db, todo_id)
    if not todo or (todo.user_id != current_user.id and getattr(current_user, 'role', 'user') != 'admin'):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="To-Do not found or not allowed")
    updates = {}
    if request.task is not None:
        updates['task'] = request.task
    if request.completed is not None:
        updates['completed'] = request.completed
    updated = todo_service.update_todo(db, todo_id, updates)
    return ToDoUpdateResponse(todo=updated)

@router.delete("/{todo_id}", response_model=ToDoDeleteResponse)
def delete_todo(todo_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    todo = todo_service.get_todo_by_id(db, todo_id)
    if not todo or (todo.user_id != current_user.id and getattr(current_user, 'role', 'user') != 'admin'):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="To-Do not found or not allowed")
    success = todo_service.delete_todo(db, todo_id)
    return ToDoDeleteResponse(success=success, message="Deleted" if success else "Not found")
