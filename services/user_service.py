from fastapi import Depends,HTTPException
from connection import connector
from typing import Annotated
from sqlalchemy.orm import Session
from models.user_model import User
from sqlalchemy import or_

class UserService:
    def __init__(self, db:Annotated[Session, Depends(connector)]):
        self.db = db
    
    async def register_user(self, email:str, user_name:str, password:str|int) -> User | HTTPException:
        db = self.db
        if db.query(User).filter(
            or_(User.email == email, User.user_name == user_name)
        ).first():
            raise HTTPException(detail="Email or User name already taken", status_code=403)
        
        user = User(
            user_name = user_name,
            password  = password,
            email     = email
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    async def login(self, user_name:str, password:str|int) -> User | None:
        return self.db.query(User).filter(
            User.user_name == user_name,
            User.password == password
        ).first()
    
    async def find_user(self, id:int) -> User | None:
        return User.active(self.db).filter(User.id==id).first()