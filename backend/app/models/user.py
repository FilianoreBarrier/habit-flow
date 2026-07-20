from __future__ import annotations
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from app.core.database import Base
from sqlalchemy import  DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
if TYPE_CHECKING:
    from .habit import Habit
    from .habit_log import HabitLog

class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username:Mapped[str] = mapped_column (index=True)
    email:Mapped[str]  = mapped_column(unique=True, index=True)
    hashed_password:Mapped[str]  = mapped_column()
    full_name:Mapped[str| None] = mapped_column ()
    is_active:Mapped[bool]  = mapped_column(default=True)
    created_at:Mapped[datetime]  = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    habits: Mapped[list[Habit]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
    habit_logs: Mapped[list[HabitLog]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.email}>"
