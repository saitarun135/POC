from pydantic import BaseModel,Field,validator

class CreateToDoRequest(BaseModel):
    title:str = Field(..., min_length=5)
    description:str
    
    @validator('description')
    def validate_description(cls, v):
        if v is not None and len(v) > 255:
            raise ValueError("description field size is 255 only.")
        return v
    