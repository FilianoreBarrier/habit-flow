from typing import List
from app.models.token_blacklist import TokenBlackList
from app.core.exceptions import raise_user_not_found
from app.core.security import get_password_hash,decode_access_token, verify_password
from app.core.config
from app.repositories.habit_repository import HabitRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.repositories.token_repository import TokenRepository
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
import jwt

class UserService:
    def __init__(self, db: AsyncSession):
         self.user_repository = UserRepository(db)
         self.habit_repository = HabitRepository(db)
         self.token_respository = TokenRepository(db)


    async def create_user(self, user_data: UserCreate) -> UserResponse:
        if await  self.user_repository.get_by_email(user_data.email):
            raise HTTPException(
                 status_code=status.HTTP_409_CONFLICT,
                 detail='The email is already taken.'
             )  # ошибка "email уже занят"
        if await self.user_repository.get_by_username(user_data.username):
            raise HTTPException(
                 status_code=status.HTTP_409_CONFLICT,
                 detail='The username is already taken'
             )  # ошибка "username уже занят"
        hashed_password = get_password_hash(user_data.password)
        user = await self.user_repository.create(user_data, hashed_password)
        return UserResponse.model_validate(user)

    async def update_user(self, user_id: int, user_update: UserUpdate) -> UserResponse:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise_user_not_found(user_id)
        updated_user = await self.user_repository.update(user_id,user_update)
        return UserResponse.model_validate(updated_user)

    async def change_password(self, user_id: int, old_password: str, new_password: str) -> UserResponse:
        """Смена пароля пользователя"""

        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise_user_not_found(user_id)

        if not verify_password(old_password, user.hashed_password):# type: ignore[attr-async defined]
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect old password"
            )

        if len(new_password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be at least 8 characters long"
            )

        new_hashed_password = get_password_hash(new_password)
        updated_user = await self.user_repository.update(user_id, UserUpdate(hashed_password= new_hashed_password))

        return UserResponse.model_validate(updated_user)


    async def authenticate_user(self, email: str, password: str) -> UserResponse:
        user = await self.user_repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User account is inactive"
            )

        return UserResponse.model_validate(user)


    async def deactivate_user(self, user_id: int) -> UserResponse:
        user = await self.user_repository.get_by_id(user_id)

        if not user:
            raise_user_not_found(user_id)

        if not user.is_active:# type: ignore[attr-async defined]
            return UserResponse.model_validate(user)

        user.is_active = False # type: ignore[attr-async defined]

        updated_user = await self.user_repository.update(user_id, UserUpdate(is_active=False))

        return UserResponse.model_validate(updated_user)

    async def list_users(self) -> List[UserResponse]:
        users = await self.user_repository.get_all()
        return [UserResponse.model_validate(user) for user in users]

    '''get methods'''
    async def get_by_id(self, user_id: int) -> UserResponse:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise_user_not_found(user_id)
        return UserResponse.model_validate(user)

    async def get_by_email(self, email: str) -> UserResponse:
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with this email not found."
            )
        return UserResponse.model_validate(user)

    async def get_by_username(self, username: str) -> UserResponse:
        user = await self.user_repository.get_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with this username not found."
            )
        return UserResponse.model_validate(user)

    async def blacklist_token(self, token: str) -> bool:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            exp_timestamp = payload.get("exp")

            if exp_timestamp is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid token payload: missing exp"
                )

            expire_time = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)

        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate token"
            )

        db_token = TokenBlackList(token=token, expires_at=expire_time)
        await self.token_respository.add_to_blacklist(db_token)

        return True
