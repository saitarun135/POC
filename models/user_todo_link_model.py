from database import Base
from sqlalchemy import Column, Integer


class UserToDOsLink(Base):
    __tablename__="user_todos_link"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    todo_id = Column(Integer, index=True, nullable=False)
    status = Column(Integer, index=True, default=0, nullable=False)
