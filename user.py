from fastapi import APIRouter,Depends
from connection import connector
from typing import Annotated
from sqlalchemy.orm import Session
from requests.user_register import Register
from requests.login_request import Login
from requests.update_email_request import UpdateEmail
from auth import Auth
from datetime import datetime
from services.user_service import UserService

user_router = APIRouter()

con = Annotated[Session, Depends(connector)]
auth_user_id = Annotated[int, Depends(Auth().id)]

@user_router.post('/register-user')
async def register_user(req:Register, db:con):
    user = await UserService(db).register_user(req.email, req.user_name, req.password)
    return {
        "success": True,
        "message": "User registration completed successfully.",
        "data":user
    }
    
@user_router.post('/login')
async def login(req:Login, db:con):
    user = await UserService(db).login(req.user_name, req.password)
    if user is None:
        return {"success":False, "message":"Invalid credentials"}
    
    payload = {
        "user_name" : user.user_name,
        "email":user.email,
        "id":user.id
    }
    
    token = Auth().encode_data(data=payload)

    return {
        "success" : True,
        "token_type":"Bearer",
        "token":token,
        "expires_at":""
    }
    
@user_router.patch('/update-user-email')
async def update_user_email(id:auth_user_id ,req:UpdateEmail, db:con):
    user = await UserService(db).find_user(id)
    if user is None:
        return {
            "success" : False,
            "message": "Record not found for the requested id."
        }
    user.email = req.email
    user.updated_at = datetime.now()
    db.commit()
    db.refresh(user)
    return {
        "success" : True,
        "message" : "Updated successfully",
        "data": {"id": user.id, "email": user.email}
    }
    
@user_router.delete('/deactivate-account')
async def deactivate_account(id:auth_user_id, db:con):
    user = await UserService(db).find_user(id)
    user.status = 1
    user.updated_at = datetime.now()
    db.commit()
    return {
        "success" : True,
        "message" : "Account de-activated successfully.all the actions will be disabled from now onwards."
    }
    