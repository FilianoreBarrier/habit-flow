from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.token_blacklist import TokenBlackList

class TokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_to_blacklist(self, db_token: TokenBlackList) -> TokenBlackList:
        """Сохраняет токен в черный список в PostgreSQL"""
        self.db.add(db_token)
        await self.db.commit()
        return db_token

    async def is_token_blacklisted(self, token: str) -> bool:
        """Проверяет, заблокирован ли токен (используется в security.py)"""
        result = await self.db.execute(
            select(TokenBlackList).where(TokenBlackList.token == token)
        )
        blacklisted_token = result.scalar_one_or_none()
        return blacklisted_token is not None
