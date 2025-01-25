from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from application.common.exception import ServiceException
from application.db.postgres.db import get_session
from application.schemas.user import (
    TokenOutSchema,
    UserLoginInSchema,
    UserRegisterInSchema,
)
from application.services.auth import AuthService, get_auth_service

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def signup(
    obj_in: UserRegisterInSchema,
    service: AuthService = Depends(get_auth_service),
    session: AsyncSession = Depends(get_session),
):
    try:
        user = await service.signup_user(session=session, obj_in=obj_in)

        return {"message": f"User {user.username} created"}

    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    obj_in: UserLoginInSchema,
    service: AuthService = Depends(get_auth_service),
    session: AsyncSession = Depends(get_session),
) -> TokenOutSchema:
    try:
        return await service.signin_user(session=session, obj_in=obj_in)
    except ServiceException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
