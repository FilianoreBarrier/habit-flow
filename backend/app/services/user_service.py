from typing import List

from app.core.security import get_password_hash, verify_password
from app.repositories.habit_repository import HabitRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


class UserService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)
        self.habit_repository = HabitRepository(db)

    def create_user(self, user_data: UserCreate) -> UserResponse:
        if self.user_repository.get_by_email(user_data.email):
            raise HTTPException(
                 status_code=status.HTTP_409_CONFLICT,
                 detail='The email is already taken.'
             )  # ошибка "email уже занят"
        if self.user_repository.get_by_username(user_data.username):
            raise HTTPException(
                 status_code=status.HTTP_409_CONFLICT,
                 detail='The username is already taken'
             )  # ошибка "username уже занят"
        hashed_password = get_password_hash(user_data.password)
        user = self.user_repository.create(user_data, hashed_password)
        return UserResponse.model_validate(user)
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> UserResponse:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'User with id {user_id} not found.'
            )
        updated_user = self.user_repository.update(user_id,user_update)
        return UserResponse.model_validate(updated_user)
    
    def change_password():
        ...

    def authenticate_user(self, email: str, password: str) -> UserResponse:
        user = self.user_repository.get_by_email(email)
        if not user:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

        if not verify_password(password, hashed_password): # type: ignore[attr-defined]
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        if not user.is_active:# type: ignore[attr-defined]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is inactive"
            )

        return UserResponse.model_validate(user)
        
        
    def deactivate_user():
        ...
    def list_users():
        ...

    '''get methods'''
    def get_by_id(self, user_id: int) -> UserResponse:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'User with id {user_id} not found.'
            )
        return UserResponse.model_validate(user)
    
    def get_by_email(self, email: str) -> UserResponse:
        user = self.user_repository.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with this email not found."
            )
        return UserResponse.model_validate(user)

    def get_by_username(self, username: str) -> UserResponse:
        user = self.user_repository.get_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with this username not found."
            )
        return UserResponse.model_validate(user)

    def get_all_users(self) -> list[UserResponse]:
        users = self.user_repository.get_all()
        return [UserResponse.model_validate(user) for user in users]
        

