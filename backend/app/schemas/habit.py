from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class HabitBase(BaseModel):
    name: str = Field(max_length=50, description="Habit name")
    description: Optional[str] = Field(None,max_length=300,description="Habit description")
    frequency: str = Field(default="daily",description='daily/weekly/monthly')

class HabitCreate(HabitBase):
    pass

class HabitResponse(HabitBase):
    id: int = Field(description="Unique habit identifier")
    user_id: int
    created_at: datetime
    is_active: bool = True
    model_config = {"from_attributes": True}

class HabitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    frequency: Optional[str] = None
