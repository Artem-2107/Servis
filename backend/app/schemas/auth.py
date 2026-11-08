from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Логин пользователя")
    password: str = Field(..., min_length=6, description="Пароль (минимум 6 символов)")
    role: Optional[str] = Field(default="manager", description="Роль: admin, manager, accountant")

class UserLogin(BaseModel):
    username: str = Field(..., description="Логин пользователя")
    password: str = Field(..., description="Пароль")

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True