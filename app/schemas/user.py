from pydantic import BaseModel,EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    name :str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    ind:int
    name :str
    email:str
    is_active:bool
    created_at:datetime

    model_config = {"from_atributes":True}
class UserUpdate(BaseModel):
    name :str |None =None
    email:EmailStr |None =None
    password:str |None =None