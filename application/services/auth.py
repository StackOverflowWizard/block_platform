from functools import cache

from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import check_password_hash, generate_password_hash

from application.common.exception import ServiceException
from application.models.user import User
from application.schemas.user import (
    TokenOutSchema,
    UserLoginInSchema,
    UserRegisterInSchema,
)


class AuthService:

    def __init__(self, authorize: AuthJWT):
        self._authorize = authorize

    async def signup_user(
        self,
        session: AsyncSession,
        obj_in: UserRegisterInSchema,
    ) -> User:
        try:
            if obj_in.password != obj_in.confirm_password:
                raise ServiceException("Passwords do not match")

            password_hash = generate_password_hash(obj_in.password)
            user = User(username=obj_in.username, password=password_hash)
            session.add(user)
            await session.commit()
            return user
        except IntegrityError as e:
            if "Key (username)" in str(e):
                raise ServiceException("User already exists")

    async def signin_user(
        self,
        session: AsyncSession,
        obj_in: UserLoginInSchema,
    ) -> User:
        try:
            stmt = select(User).where(User.username == obj_in.username)
            user = await session.execute(stmt)

            user = user.scalars().one()

            if not check_password_hash(user.password, obj_in.password):
                raise ServiceException("Incorrect password")

            access_token = await self._authorize.create_access_token(
                subject=user.username
            )
            refresh_token = await self._authorize.create_refresh_token(
                subject=user.username
            )

            token = TokenOutSchema(
                access_token=access_token, refresh_token=refresh_token
            )
            return token
        except NoResultFound as e:
            raise ServiceException("User not found")


@cache
def get_auth_service(
    authorize: AuthJWT = Depends(),
) -> AuthService:
    return AuthService(authorize=authorize)
