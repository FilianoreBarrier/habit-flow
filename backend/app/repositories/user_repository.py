
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[User]:
        stmt = select(User).options(selectinload(User.habits))
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def get_by_id(self,user_id:int) -> User | None:
        return await self.db.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        return await self.db.scalar(select(User).where(User.email == email))

    async def get_by_username(self, username: str) -> User | None:
        return await self.db.scalar(select(User).where(User.username == username))

    async def create(self, user_data: UserCreate, hashed_password: str) -> User:
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            is_active=True
        )
        self.db.add(db_user)
        await self.db.commit()   # Добавили await
        await self.db.refresh(db_user) # Добавили await
        return db_user

    async def update(self, user_id: int, user_update: UserUpdate) -> User | None:
        user = await self.get_by_id(user_id)
        if user:
            update_data = user_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(user, key, value)
            await self.db.commit()   # Добавили await
            await self.db.refresh(user) # Добавили await
        return user

    async def get_multiple_by_ids(self, user_ids: list[int])-> list[User]:
        stmt = select(User).where(User.user_id.in_(user_ids))
        result = await self.db.scalars(stmt)
        return list(result.all())
