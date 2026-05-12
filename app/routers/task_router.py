from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.db_manager import get_db
from app.models.user import User
from app.models.session import Session as SessionModel, SessionStatus
from app.models.tasks_models import Task
from app.models.comentarios import Comentario
from app.schemas.tasks_schemas import TaskCreate, TaskClose, TaskResponse
from app.schemas.comments import ComentarioCreate, ComentarioResponse
from app.core.dependencies import get_current_user

# Definição clara dos roteadores
task_router = APIRouter(prefix="/tasks", tags=["Tasks"])
comments_router = APIRouter(prefix="/comments", tags=["Comments"])

@task_router.post("/create", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(SessionModel).filter(
        SessionModel.user_id == current_user.id,
        SessionModel.status == SessionStatus.open
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você precisa ter uma sessão aberta para criar tarefas."
        )

    new_task = Task(
        session_id=session.id,
        titulo=data.titulo,
        tipo=data.tipo
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# Removido o prefixo redundante no path
@task_router.get("/list", response_model=list[TaskResponse])
def list_my_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Task).join(SessionModel).filter(
        SessionModel.user_id == current_user.id
    ).all()

@task_router.patch("/{task_id}/close", response_model=TaskResponse)
def close_task(
    task_id: str,
    data: TaskClose,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).join(SessionModel).filter(
        Task.id == task_id,
        SessionModel.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    task.closed_at = datetime.utcnow()
    task.nivel_foco = data.nivel_foco
    db.commit()
    db.refresh(task)
    return task

# Corrigido para usar @comments_router
@comments_router.post("/{task_id}/add", response_model=ComentarioResponse)
def add_comment(
    task_id: str,
    data: ComentarioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).join(SessionModel).filter(
        Task.id == task_id,
        SessionModel.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    novo_comentario = Comentario(
        task_id=task_id,
        titulo=data.titulo,
        tipo=data.tipo,
        conteudo=data.conteudo
    )
    db.add(novo_comentario)
    db.commit()
    db.refresh(novo_comentario)
    return novo_comentario