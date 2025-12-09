from fastapi import APIRouter,Depends,Path
from typing import Annotated
from auth import Auth
from connection import connector
from sqlalchemy.orm import Session
from requests.create_todo_request import CreateToDoRequest
from datetime import datetime
from services.todo_service import ToDoService


todo_router = APIRouter()
auth_usr = Annotated[int,Depends(Auth().id)]
con = Annotated[Session, Depends(connector)]

@todo_router.post('/create')
async def create_to_do(id:auth_usr, req:CreateToDoRequest, db:con):
    todo = await ToDoService(db, id).create_to_do(req.title, req.description)
    return {
        "success" : True,
        "message" : "Created Successfully.",
        "data" : todo
    }

@todo_router.patch('/share-with/{from_todo_id}/{to_user_id}')
async def share_with(from_todo_id:int, to_user_id:int, id:auth_usr, db:con):
    alreadyShared = ToDoService(db, id).already_collabarated_with_user(from_todo_id, to_user_id)
    if alreadyShared:
        alreadyShared.status = 0
        alreadyShared.commit()
        return {
            "success" : True,
            "message" : "To DO shared successfully."
        }
    
    await ToDoService(db, id).collabarate_with_user(to_user_id, from_todo_id)
    return {
        "success" : True,
        "message" : "To DO shared successfully."
    }
    
@todo_router.patch('/remove-user/{from_todo_id}/{to_user_id}')
async def remove_user(from_todo_id:int, to_user_id:int, id:auth_usr, db:con):
    fromToDO = ToDoService(db, id).find_todo(from_todo_id)
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
    
    
    link = ToDoService(db,id).unlink_user(to_user_id, from_todo_id)
    
    return {
        "success" : True,
        "message" : "Successfully removed user.",
        "link_status": link
    }
    
@todo_router.delete('/delete/{to_do_id}')
async def delete(id:auth_usr, db:con, to_do_id:int=Path(gt=0)):
    toDo = ToDoService(db, id).find_todo(to_do_id)
    
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
    
    