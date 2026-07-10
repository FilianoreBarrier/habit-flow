from datetime import datetime

from app.core.database import Base
from sqlalchemy import (Boolean, Column, Date, DateTime, ForeignKey, Integer,
                        Text)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class HabitLog(Base):
    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True, index=True)

    # Связи
    habit_id = Column(Integer, ForeignKey("habits.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    # Основные данные
    date = Column(Date, nullable=False, index=True)           # дата выполнения
    completed = Column(Boolean, default=True, nullable=False) # выполнена ли привычка
    note = Column(Text, nullable=True)                        # заметка (опционально)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    habit = relationship("Habit", back_populates="logs")
    user = relationship("User", back_populates="habit_logs")

    def __repr__(self):
        return f"<HabitLog(habit_id={self.habit_id}, date={self.date}, completed={self.completed})>"
