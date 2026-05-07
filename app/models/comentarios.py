from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db_manager import Base
import enum

class TipoComentario(enum.Enum):
    comentario='comentario'
    ocorrencia='ocorrencia'

class Comentario(Base):
    __tablename__='comentarios'
    id=Column(Integer, primary_key=True,nullable=False,index=True,autoincrement=True)
    titulo=Column(String(100),nullable=False)
    task_id=Column(String,ForeignKey('tasks.id'),nullable=False)
    tipo=Column(Enum(TipoComentario), nullable=False)
    conteudo=Column(String(1000),nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow,nullable=False)

    task=relationship("Task",back_populates="comentarios")
