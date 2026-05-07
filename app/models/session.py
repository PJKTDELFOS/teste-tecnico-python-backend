from sqlalchemy import Column, String, Integer,Boolean,DateTime,ForeignKey,Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db_manager import Base
import enum



class SessionStatus(enum.Enum):
    open="open"
    closed="closed"


class Session(Base):
    __tablename__ = "sessions"
    id=Column(Integer, primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    status=Column(Enum(SessionStatus),nullable=False,default=SessionStatus.open)
    start_at=Column(DateTime,nullable=False,default=datetime.utcnow)
    end_at=Column(DateTime)

    owner=relationship("User",back_populates="sessions")
    tasks=relationship("Task",back_populates="session",cascade="all,delete-orphan")