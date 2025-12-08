from database import Base
from sqlalchemy import Column,Integer,String,DateTime
# from datetime import datetime,timezone
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True, index=True)
    user_name = Column(String(20), nullable=False)
    password = Column(String(60), nullable=False)
    email=Column(String(255),nullable=False, unique=True)
    status=Column(Integer,default=0, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at=Column(DateTime,nullable=True)
    
    @classmethod
    def active(cls, db):
        return db.query(cls).filter(cls.status == 0)