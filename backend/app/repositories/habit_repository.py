from app.models.habit import Habit
from app.schemas.habit import HabitCreate, HabitUpdate
from sqlalchemy import select
from sqlalchemy.orm import Session


class HabitRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: int) -> list[Habit]:
        result = self.db.execute(
            select(Habit).where(Habit.user_id == user_id)
        )
        return list(result.scalars().all())

    def get_by_id(self, habit_id: int) -> Habit | None:
        return self.db.get(Habit, habit_id)

    def create(self, habit_data: HabitCreate, user_id: int) -> Habit:
        db_habit = Habit(**habit_data.model_dump(),
                         user_id = user_id,
                         is_active = True)
        self.db.add(db_habit)
        self.db.commit()
        self.db.refresh(db_habit)
        return db_habit
    
    def update(self, habit_id: int, habit_update: HabitUpdate) -> Habit | None:
        habit = self.get_by_id(habit_id)
        if habit:
            update_data = habit_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(habit, key, value)
            self.db.commit()
            self.db.refresh(habit)
        return habit
    
    def delete(self, habit_id: int) -> bool:
        habit = self.get_by_id(habit_id)
        if habit:
            self.db.delete(habit)
            self.db.commit()
            return True
        return False