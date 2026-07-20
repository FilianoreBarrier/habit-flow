from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime, timezone
from app.core.database import Base
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
if TYPE_CHECKING:
    from .user import User
    from .habit_log import HabitLog

class Habit(Base):
    __tablename__ = "habits"

    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    # Связь с пользователем
    user_id:Mapped[int] = mapped_column(ForeignKey("users.user_id"), index=True)

    name:Mapped[str] = mapped_column(index=True)
    description:Mapped[str|None] = mapped_column()
    # Как часто нужно выполнять привычку
    frequency:Mapped[str] = mapped_column(default="daily")  # daily, weekly, custom и т.д.

    is_active:Mapped[bool] = mapped_column(default=True)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Связь обратно с пользователем
    user: Mapped[User]= relationship(back_populates="habits")
    logs: Mapped[list[HabitLog]] = relationship(back_populates="habit", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Habit {self.name} (user_id={self.user_id})>"
