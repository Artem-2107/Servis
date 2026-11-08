
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import AuthService
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


# Регистрация пользователя
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    return await service.register(data)


# Авторизация пользователя
@router.post(
    "/login",
    response_model=Token
)
async def login_user(
    data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)

    return await service.login(
        username=data.username,
        password=data.password
    )


# Получение информации о текущем пользователе
@router.get(
    "/me",
    response_model=UserResponse
)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    return current_user
