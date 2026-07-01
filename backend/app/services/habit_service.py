from typing import List

from app.core.exceptions import raise_user_not_found
from app.repositories.habit_repository import HabitRepository
from app.repositories.user_repository import UserRepository
from app.schemas.habit import HabitCreate, HabitResponse, HabitUpdate
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


class HabitService:
    def __init__(self, db: Session):
        self.habit_repository = HabitRepository(db)
        self.user_repository = UserRepository(db)   # может понадобиться для проверок

    def create_habit(self, habit_data: HabitCreate, user_id: int) -> HabitResponse:
        # Здесь должна быть логика:
        # - проверить, существует ли пользователь
        # - проверить лимит привычек у пользователя (опционально)
        # - создать привычку
        ...

    def get_user_habits(self, user_id: int) -> list[HabitResponse]:
        ...

    def get_habit_by_id(self, habit_id: int) -> HabitResponse:
        ...

    def update_habit(self, habit_id: int, habit_update: HabitUpdate) -> HabitResponse:
        ...

    def delete_habit(self, habit_id: int) -> bool:
        ...