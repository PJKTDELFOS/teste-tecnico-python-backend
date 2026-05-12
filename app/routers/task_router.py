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

task_router = APIRouter(prefix="/tasks", tags=["tasks"])
comments_router = APIRouter(prefix="/tasks", tags=["comentarios"])

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

def get_task_do_usuario(task_id: str, current_user: User, db: Session) -> Task:
    task = db.query(Task).join(SessionModel).filter(
        Task.id == task_id,
        SessionModel.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task nao encontrada"
        )
    return task

# ─── TASKS ────────────────────────────────────────────

@task_router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = get_active_session(current_user, db)
    task = Task(
        session_id=session.id,
        titulo=data.titulo,
        tipo=data.tipo,
        tempo_minutos=data.tempo_minutos
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@task_router.get("/", response_model=list[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = get_active_session(current_user, db)
    return db.query(Task).filter(Task.session_id == session.id).all()

@task_router.get("/{task_id}", response_model=TaskResponse)
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
        raise HTTPException(status_code=404, detail="Task nao encontrada")
    return task

@task_router.patch("/{task_id}/nivel-foco", response_model=TaskResponse)
def update_nivel_foco(
    task_id: str,
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = get_active_session(current_user, db)
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.session_id == session.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task nao encontrada")
    if task.closed_at is not None:
        raise HTTPException(status_code=400, detail="Task ja encerrada")
    task.nivel_foco = data.nivel_foco
    db.commit()
    db.refresh(task)
    return task

@task_router.post("/{task_id}/close", response_model=TaskResponse)
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
        raise HTTPException(status_code=404, detail="Task nao encontrada")
    if task.closed_at is not None:
        raise HTTPException(status_code=400, detail="Task ja encerrada")
    task.nivel_foco = data.nivel_foco
    task.tempo_minutos = data.tempo_minutos
    task.closed_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task

# ─── COMENTARIOS ──────────────────────────────────────

@comments_router.post("/{task_id}/comentarios", response_model=ComentarioResponse, status_code=status.HTTP_201_CREATED)
def create_comentario(
    task_id: str,
    data: ComentarioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = get_task_do_usuario(task_id, current_user, db)
    comentario = Comentario(
        task_id=task.id,
        titulo=data.titulo,
        tipo=data.tipo,
        conteudo=data.conteudo
    )
    db.add(comentario)
    db.commit()
    db.refresh(comentario)
    return comentario

@comments_router.get("/{task_id}/comentarios", response_model=list[ComentarioResponse])
def list_comentarios(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = get_task_do_usuario(task_id, current_user, db)
    return db.query(Comentario).filter(Comentario.task_id == task.id).all()

@comments_router.delete("/{task_id}/comentarios/{comentario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comentario(
    task_id: str,
    comentario_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = get_task_do_usuario(task_id, current_user, db)
    comentario = db.query(Comentario).filter(
        Comentario.id == comentario_id,
        Comentario.task_id == task.id
    ).first()
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentario nao encontrado")
    db.delete(comentario)
    db.commit()