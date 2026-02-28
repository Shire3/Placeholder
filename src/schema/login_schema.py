from pydantic import BaseModel, EmailStr, Field
from typing_extensions import Literal 

class loginRequest(BaseModel):
    email:EmailStr = Field()
    password: str = Field()


class loginResponse(BaseModel):
    email: EmailStr
    role: Literal["user", "admin"]
    access_token: str
    refresh_token: str