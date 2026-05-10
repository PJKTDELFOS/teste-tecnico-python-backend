from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.db_manager import get_db
from app.models.user import User
from app.models.session import Session as SessionModel, SessionStatus
from app.models.tasks import Task
from app.schemas.tasks import TaskCreate, TaskClose, TaskUpdate, TaskResponse
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_active_session(current_user: User, db: Session) -> SessionModel:
    session = db.query(SessionModel).filter(
        SessionModel.user_id == current_user.id,
        SessionModel.status == SessionStatus.open
    ).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhuma session ativa — abra uma session primeiro"
        )
    return session

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = get_active_session(current_user, db)
    task = Task(
        session_id=session.id,
        titulo=data.titulo,
        tipo=data.tipo
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = get_active_session(current_user, db)
    return db.query(Task).filter(Task.session_id == session.id).all()

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = get_active_session(current_user, db)
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.session_id == session.id
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task não encontrada"
        )
    return task

@router.patch("/{task_id}/nivel-foco", response_model=TaskResponse)
def update_nivel_foco(
    task_id: str,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = get_active_session(current_user, db)
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.session_id == session.id
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task não encontrada"
        )
    if task.closed_at is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task já encerrada"
        )
    task.nivel_foco = data.nivel_foco
    db.commit()
    db.refresh(task)
    return task

@router.post("/{task_id}/close", response_model=TaskResponse)
def close_task(
    task_id: str,
    data: TaskClose,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = get_active_session(current_user, db)
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.session_id == session.id
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task não encontrada"
        )
    if task.closed_at is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task já encerrada"
        )
    task.nivel_foco = data.nivel_foco
    task.closed_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task