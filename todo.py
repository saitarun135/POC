from fastapi import APIRouter,Depends,Path
from typing import Annotated
from auth import Auth
from connection import connector
from sqlalchemy.orm import Session
from requests.create_todo_request import CreateToDoRequest
from models.todo_model import ToDoModel
from models.user_todo_link_model import UserToDOsLink
from datetime import datetime


todo_router = APIRouter()
auth_usr = Annotated[int,Depends(Auth().id)]
con = Annotated[Session, Depends(connector)]

@todo_router.post('/create')
async def create_to_do(id:auth_usr, req:CreateToDoRequest, db:con):
    todo = ToDoModel(
            title = req.title,
            description = req.description,
            created_by = id
        )
    db.add(todo)
    db.commit()
    
    return {
        "success" : True,
        "message" : "Created Successfully.",
        "data" : todo
    }

@todo_router.patch('/share-with/{from_todo_id}/{to_user_id}')
async def share_with(from_todo_id:int, to_user_id:int, db:con):
    alreadyShared = db.query(UserToDOsLink).filter(UserToDOsLink.todo_id == from_todo_id, UserToDOsLink.user_id == to_user_id).first()
    
    if alreadyShared:
        alreadyShared.status = 0
        alreadyShared.commit()
        
        return {
            "success" : True,
            "message" : "To DO shared successfully."
        }
    
    link = UserToDOsLink(
        user_id = to_user_id,
        todo_id = from_todo_id
    )
    
    db.add(link)
    db.commit()
    return {
        "success" : True,
        "message" : "To DO shared successfully."
    }
    
@todo_router.patch('/remove-user/{from_todo_id}/{to_user_id}')
async def remove_user(from_todo_id:int, to_user_id:int, id:auth_usr, db:con):
    fromToDO = db.query(ToDoModel).filter(ToDoModel.id == from_todo_id).first()
    if not fromToDO:
        return {
            "success": False,
            "message":"Record not found."
        }
    elif fromToDO.created_by != id:
        return {
            "success":False,
            "message":"You are not the owner of this todo inorder to remove."
        }
    
    
    link = db.query(UserToDOsLink).filter(UserToDOsLink.user_id == to_user_id, UserToDOsLink.todo_id == from_todo_id, UserToDOsLink.status == 0).first()
    link.status =0
    link.commit()
    
    return {
        "success" : True,
        "message" : "Successfully removed user."
    }
    
@todo_router.delete('/delete/{to_do_id}')
async def delete(id:auth_usr, db:con, to_do_id:int=Path(gt=0)):
    toDo = db.query(ToDoModel).filter(ToDoModel.id == to_do_id, ToDoModel.status == 0).first()
    
    if not toDo:
        return {
            "success" : False,
            "message" : "Record not found or it might delete earlier."
        }
    elif toDo.created_by != id:
        return {
            "success" : False,
            "message" : "You are not the owner of this To DO."
        }
    
    toDo.status = 1
    toDo.updated_by = id
    toDo.updated_at = datetime.now()
    toDo.commit()

    return {
        "success" : True,
        "message" : "To DO is deleted and successfully removed for the collbarative users aswell."
    }
    
    