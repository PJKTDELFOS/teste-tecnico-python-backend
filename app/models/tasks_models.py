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
    nivel_foco=Column(Integer,nullable=True)
    tipo=Column(Enum(TipoTask), nullable=False)
    opened_at=Column(DateTime,default=datetime.utcnow,nullable=False)
    closed_at=Column(DateTime,nullable=True)
    tempo_minutos = Column(Integer, nullable=True)


    __table_args__=(
        CheckConstraint("nivel_foco >=1 AND nivel_foco <=5",name="nivel_foco de 1 a 5"),
    )

    session=relationship("Session",back_populates="tasks")
    comments=relationship("Comentario",back_populates="task",cascade="all,delete-orphan" )