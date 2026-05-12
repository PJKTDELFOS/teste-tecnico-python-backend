from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.db_manager import get_db
from app.models.user import User
from app.models.session import Session as SessionModel, SessionStatus
from app.schemas.session import SessionResponse
from app.core.dependencies import get_current_user
from app.models.tasks_models import Task

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def open_session(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # verifica se já tem session aberta
    open_session = db.query(SessionModel).filter(
        SessionModel.user_id == current_user.id,
        SessionModel.status == SessionStatus.open
    ).first()

    # se tiver, fecha automaticamente
    if open_session:
        open_session.status = SessionStatus.closed
        open_session.end_at = datetime.utcnow()

        # fecha todas as tasks abertas sem nivel_foco com default 3
        for task in open_session.tasks:
            if task.closed_at is None:
                task.closed_at = datetime.utcnow()
                if task.nivel_foco is None:
                    task.nivel_foco = 3

        db.commit()

    # abre nova session
    new_session = SessionModel(user_id=current_user.id)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@router.get("/", response_model=list[SessionResponse])
def list_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(SessionModel).filter(
        SessionModel.user_id == current_user.id
    ).all()

@router.get("/active", response_model=SessionResponse)
def get_active_session(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(SessionModel).filter(
        SessionModel.user_id == current_user.id,
        SessionModel.status == SessionStatus.open
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhuma session ativa"
        )
    return session

@router.post("/close", response_model=SessionResponse)
def close_session(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(SessionModel).filter(
        SessionModel.user_id == current_user.id,
        SessionModel.status == SessionStatus.open
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhuma session ativa para fechar"
        )

    session.status = SessionStatus.closed
    session.end_at = datetime.utcnow()

    # fecha todas as tasks abertas sem nivel_foco com default 3
    for task in session.tasks:
        if task.closed_at is None:
            task.closed_at = datetime.utcnow()
            if task.nivel_foco is None:
                task.nivel_foco = 3

    db.commit()
    db.refresh(session)
    return session

@router.get("/{session_id}", response_model=SessionResponse)
def get_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session não encontrada"
        )
    return session