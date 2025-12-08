from pydantic import BaseModel,Field

class Login(BaseModel):
    user_name:str = Field(...,min_length=3)
    password:str = Field(...,min_length=3)