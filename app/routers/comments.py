from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db_manager import get_db
from app.models.user import User
from app.models.session import Session as SessionModel
from app.models.tasks import Task
from app.models.comentarios import Comentario
from app.schemas.comments import ComentarioCreate, ComentarioResponse
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_task_do_usuario(task_id: str, current_user: User, db: Session) -> Task:
    task = db.query(Task).join(SessionModel).filter(
        Task.id == task_id,
        SessionModel.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task não encontrada"
        )
    return task

@router.post("/{task_id}/comentarios", response_model=ComentarioResponse, status_code=status.HTTP_201_CREATED)
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

@router.get("/{task_id}/comentarios", response_model=list[ComentarioResponse])
def list_comentarios(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = get_task_do_usuario(task_id, current_user, db)
    return db.query(Comentario).filter(Comentario.task_id == task.id).all()

@router.delete("/{task_id}/comentarios/{comentario_id}", status_code=status.HTTP_204_NO_CONTENT)
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comentário não encontrado"
        )
    db.delete(comentario)
    db.commit()