from app.core.exceptions import raise_habit_not_found, raise_user_not_found
from app.repositories.habit_repository import HabitRepository
from app.repositories.user_repository import UserRepository
from app.schemas.habit import HabitCreate, HabitResponse, HabitUpdate
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


class HabitService:
    def __init__(self, db: AsyncSession):
        self.habit_repository = HabitRepository(db)
        self.user_repository = UserRepository(db)   # может понадобиться для проверок

    async def create_habit(self, habit_data: HabitCreate, user_id: int) -> HabitResponse:
        if not await self.user_repository.get_by_id(user_id):
            raise_user_not_found(user_id)
        habit = await self.habit_repository.create(habit_data, user_id)
        return HabitResponse.model_validate(habit)


    async def get_user_habits(self, user_id: int) -> list[HabitResponse]:
        if not await self.user_repository.get_by_id(user_id):
            raise_user_not_found(user_id)
        habits = await self.habit_repository.get_by_user_id(user_id)
        return [HabitResponse.model_validate(habit) for habit in habits]

    async def get_habit_by_id(self, habit_id: int, user_id: int) -> HabitResponse:
        user = await self.user_repository.get_by_id(user_id)
        habit = await self.habit_repository.get_by_id(habit_id)
        if not user:
            raise_user_not_found(user_id)
        if not habit or habit.user_id != user_id:# type: ignore[attr-async defined]
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = 'Habit not found or you dont have access to it '
            )
        return HabitResponse.model_validate(habit)

    async def update_habit(self, habit_id: int, habit_update: HabitUpdate, user_id: int) -> HabitResponse:
        habit = await self.habit_repository.get_by_id(habit_id)
        if not habit:
            raise_habit_not_found(habit_id)
        if habit.user_id != user_id: # type: ignore[attr-async defined]
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = 'You can only update own habits! '
            )
        updated_habit = await self.habit_repository.update(habit_id, habit_update)
        return HabitResponse.model_validate(updated_habit)

    async def delete_habit(self, habit_id: int, user_id: int) -> bool:
        habit = await self.habit_repository.get_by_id(habit_id)
        if not habit:
            raise_habit_not_found(habit_id)
        if habit.user_id != user_id: # type: ignore[attr-async defined]
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = 'You can only delete own habits! '
            )
        self.habit_repository.delete(habit_id)
        return True
