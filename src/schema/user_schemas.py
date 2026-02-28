from pydantic import BaseModel, EmailStr, Field

class SignUpRequest(BaseModel):
    username:str = Field()
    email: EmailStr =Field()
    phone: str= Field(...,min_lenght=10, max_lenght=15)
    password: str= Field(..., min_lenght=6)
    role: str= Field(default='user')