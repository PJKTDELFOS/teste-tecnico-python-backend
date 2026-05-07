from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,CheckConstraint,Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db_manager import Base
import uuid
import enum

class TipoTask(enum.Enum):
    coding='codando'
    meeting='meeting'
    estudo='estudo'
    projeto='projeto'

class Task(Base):
    __tablename__="tasks"

    id = Column(String,primary_key=True,nullable=False,default=lambda: str(uuid.uuid4()))
    session_id = Column(Integer,ForeignKey("sessions.id"),nullable=False)
    titulo=Column(String(100),nullable=False)
    nota=Column(Integer,nullable=True)
    tipo=Column(Enum(TipoTask), nullable=False)
    opened_at=Column(DateTime,default=datetime.utcnow,nullable=False)
    closed_at=Column(DateTime,nullable=True)


    __table_args__=(
        CheckConstraint("nota >=1 AND nota <=5",name="Nota de 1 a 5"),
    )

    session=relationship("Session",back_populates="tasks")
    comments=relationship("Comentario",back_populates="task",cascade="all,delete-orphan" )