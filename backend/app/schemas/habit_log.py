from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class HabitLogBase(BaseModel):
    cr_date: date= Field(description="Habit creation date ")
    completed: bool = Field(default=True,description="Tracking habit completion")
    note: Optional[str] = Field(None,max_length=100,description='Note')
class HabitLogCreate(HabitLogBase):
    pass

class HabitLogResponse(HabitLogBase):
    id: int
    habit_id: int
    user_id: int
    created_at: datetime
    model_config = {"from_attributes":True}

class HabitLogUpdate(BaseModel):
    completed: Optional[bool] = None
    note: Optional[str] = None
