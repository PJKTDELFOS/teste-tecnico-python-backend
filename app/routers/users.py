from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db_manager import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.core.security import hash_password
from app.core.dependencies import get_current_user
from app.models.tasks_models import Task
from app.models.session import Session as SessionModel
from sqlalchemy import func



router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=UserResponse)
def update_me(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if data.name is not None:
        current_user.name = data.name
    if data.email is not None:
        existing = db.query(User).filter(User.email == data.email).first()
        if existing and existing.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
        current_user.email = data.email
    if data.password is not None:
        current_user.hashed_password = hash_password(data.password)

    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db.delete(current_user)
    db.commit()



@router.get("/me/diagnostico-produtividade")
def diagnostico_produtividade(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tasks = db.query(Task).join(SessionModel).filter(
        SessionModel.user_id == current_user.id,
        Task.nivel_foco != None
    ).all()

    if not tasks:
        return {
            "total_tasks": 0,
            "media_nivel_foco": None,
            "tempo_total_minutos": 0,
            "feedback": "Nenhuma tarefa registrada ainda."
        }

    total = len(tasks)
    media = sum(t.nivel_foco for t in tasks) / total
    tempo_total = sum(t.tempo_minutos for t in tasks if t.tempo_minutos)

    if media < 2:
        feedback = "Pausas mais longas e menos notificações."
    elif media < 3:
        feedback = "Tente blocos de foco de 25 minutos com a técnica Pomodoro."
    elif media < 4:
        feedback = "Bom ritmo! Mantenha o ambiente organizado."
    else:
        feedback = "Você está em uma maratona produtiva de alto nível!"

    return {
        "total_tasks": total,
        "media_nivel_foco": round(media, 2),
        "tempo_total_minutos": tempo_total,
        "feedback": feedback
    }