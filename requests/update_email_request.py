from pydantic import BaseModel, Field, EmailStr

class UpdateEmail(BaseModel):
    email:EmailStr = Field(...)