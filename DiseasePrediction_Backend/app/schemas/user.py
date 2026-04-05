from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    age: int
    phone: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ResetPassword(BaseModel):
    email: EmailStr
    new_password: str