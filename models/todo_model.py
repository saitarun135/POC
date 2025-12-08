from database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

class ToDoModel(Base) :
    __tablename__="to_dos"
    id = Column(Integer, primary_key= True)
    title = Column(String(50), nullable=False)
    description = Column(String(500), nullable=True)
    status = Column(Integer, default=0, index=True, nullable=False)
    created_by = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default= func.now(),nullable=False)
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime, server_default= func.now(),nullable=True)
    
