from typing import List, Optional

from app.models.habit import Habit
from app.schemas.habit import HabitCreate
from sqlalchemy.orm import Session


class HabitRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Habit]:
        return self.db.query(Habit).all()

    def get_by_id(self, habit_id: int) -> Optional[Habit]:
        return self.db.query(Habit).filter(Habit.id == habit_id).first()

    def get_by_slug(self, name: str) -> Optional[Habit]:
        return self.db.query(Habit).filter(Habit.name == name).first()

    def create(self, habit_data: HabitCreate) -> Habit:
        db_habit = Habit(**habit_data.model_dump())
        self.db.add(db_habit)
        self.db.commit()
        self.db.refresh(db_habit)
        return db_habit
