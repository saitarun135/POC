from fastapi import Depends
from typing import Annotated
from connection import connector
from sqlalchemy.orm import Session
from models.todo_model import ToDoModel
from models.user_todo_link_model import UserToDOsLink


class ToDoService:
    def __init__(self, db:Annotated[Session, Depends(connector)], user_id:int):
        self.db = db
        self.user_id = user_id
        
    async def create_to_do(self, title:str|int, description:str) -> ToDoModel:
        todo = ToDoModel(
            title = title,
            description = description,
            created_by = self.user_id
        )
        self.db.add(todo)
        self.db.commit()
        return todo
    
    async def already_collabarated_with_user(self, from_todo_id:int, to_user_id:int):
        return self.db.query(UserToDOsLink).filter(UserToDOsLink.todo_id == from_todo_id, UserToDOsLink.user_id == to_user_id).first()
    
    async def collabarate_with_user(self, to_user_id:int, from_todo_id:int):
        link = UserToDOsLink(
            user_id = to_user_id,
            todo_id = from_todo_id
        )
        
        self.add(link)
        self.commit()
        return link
    
    async def find_todo(self, id:int):
        self.db.query(ToDoModel).filter(ToDoModel.id == id).first()
        
    async def unlink_user(self, to_user_id:int, from_todo_id:int):
        link = self.db.query(UserToDOsLink).filter(UserToDOsLink.user_id == to_user_id, UserToDOsLink.todo_id == from_todo_id, UserToDOsLink.status == 0).first()
        link.status = 1
        link.commit()
        return link