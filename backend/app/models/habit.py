from datetime import datetime, timezone

from app.core.database import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    # Связь с пользователем
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)

    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    # Как часто нужно выполнять привычку
    frequency = Column(String, default="daily")  # daily, weekly, custom и т.д.

    # Дополнительные настройки
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Связь обратно с пользователем
    user = relationship("User", back_populates="habits")
    logs = relationship("HabitLog", back_populates="habit", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Habit {self.name} (user_id={self.user_id})>"
