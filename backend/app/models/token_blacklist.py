from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class TokenBlackList(Base):
    __tablename__ = 'token_blacklist'
    id: Mapped[int] = mapped_column(primary_key=True,index=True)
    token: Mapped[str] = mapped_column(String(500),index=True, unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime)
