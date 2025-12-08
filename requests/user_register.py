from pydantic import BaseModel,Field,EmailStr,validator


class Register(BaseModel):
    user_name:str = Field(..., max_length=15)
    password:str = Field(...,min_length=3)
    confirm_password:str = Field(...,min_length=3)
    email:EmailStr=Field(...)
    
    @validator('confirm_password')
    def validate_pass_code(cls, V, values):
        if values['password'] != V:
            raise ValueError("Passwords do not match.")
        return V
    