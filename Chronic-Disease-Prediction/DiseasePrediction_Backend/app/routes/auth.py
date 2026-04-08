from fastapi import APIRouter
from app.schemas.user import UserCreate, UserLogin, ResetPassword
from app.schemas.auth_schema import ForgotPassword, ResetPassword
from app.services.auth_service import (
    register_user,
    login_user,
    forgot_password,
    reset_password
)

router = APIRouter()

@router.post("/register")
def register(data: UserCreate):
    return register_user(data)

@router.post("/login")
def login(data: UserLogin):
    return login_user(data)

@router.post("/forgot-password")
def forgot(data: ForgotPassword):
    return forgot_password(data.email)

@router.post("/reset-password")
def reset(data: ResetPassword):
    return reset_password(data)