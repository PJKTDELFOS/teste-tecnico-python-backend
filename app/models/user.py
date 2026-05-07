from sqlalchemy import Column, String, Integer,Boolean,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db_manager import Base


class User(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(100),nullable=False)
    email=Column(String(100),nullable=False,unique=True,index=True)
    hashed_password = Column(String(100),nullable=False)
    is_active = Column(Boolean,default=True)
    created_at = Column(DateTime,default=datetime.utcnow)

    sessions= relationship('Session',back_populates='owner',cascade="all, delete-orphan")