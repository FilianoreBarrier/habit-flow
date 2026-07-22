from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime,date
if TYPE_CHECKING:
    from .user import User
    from .habit import Habit

from app.core.database import Base
from sqlalchemy import (DateTime, ForeignKey,Text, DATE)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func


class HabitLog(Base):
    __tablename__ = "habit_logs"

    id:Mapped[int] = mapped_column(primary_key=True, index=True)

    # Связи
    habit_id:Mapped[int] = mapped_column(ForeignKey("habits.id", ondelete="CASCADE"), )
    user_id:Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), )

    cr_date:Mapped[date] = mapped_column(DATE,index=True,default=date.today)           # дата выполнения
    completed:Mapped[bool] = mapped_column(default=True, ) # выполнена ли привычка
    note:Mapped[str| None] = mapped_column(Text)                        # заметка (опционально)

    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    habit:Mapped[Habit] = relationship(back_populates="logs")
    user: Mapped[User] = relationship(back_populates="habit_logs")

    def __repr__(self):
        return f"<HabitLog(habit_id={self.habit_id}, date={self.date}, completed={self.completed})>"
