from app.models.habit import Habit
from app.schemas.habit import HabitCreate, HabitUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession



class HabitRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user_id(self, user_id: int) -> list[Habit]:
        result = await self.db.execute(
            select(Habit).where(Habit.user_id == user_id)
        )
        return list(result.scalars().all())

    async def get_by_id(self, habit_id: int) -> Habit | None:
        return await self.db.get(Habit, habit_id)

    async def create(self, habit_data: HabitCreate, user_id: int) -> Habit:
        db_habit = Habit(**habit_data.model_dump(),
                         user_id = user_id,
                         is_active = True)
        self.db.add(db_habit)
        await self.db.commit()
        await self.db.refresh(db_habit)
        return db_habit

    async def update(self, habit_id: int, habit_update: HabitUpdate) -> Habit | None:
        habit = await self.get_by_id(habit_id)
        if habit:
            update_data = habit_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(habit, key, value)
            await self.db.commit()
            await self.db.refresh(habit)
        return habit

    async def delete(self, habit_id: int) -> bool:
        habit = await self.get_by_id(habit_id)
        if habit:
            await self.db.delete(habit)
            await self.db.commit()
            return True
        return False
