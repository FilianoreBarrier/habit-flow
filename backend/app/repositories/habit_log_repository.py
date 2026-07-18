from app.models.habit_log import HabitLog
from app.schemas.habit_log import HabitLogCreate, HabitLogUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class HabitLogRepository:
        def __init__(self,db:AsyncSession):
            self.db = db

        async def get_by_id(self,log_id:int) -> HabitLog| None:
              return await self.db.get(HabitLog, log_id)

        async def get_by_completed(self, completed:bool) -> HabitLog| None:
              return await self.db.scalar(select(HabitLog).where(HabitLog.completed == completed))

        async def get_by_user_id(self, user_id: int) -> list[HabitLog]:
            result = await self.db.scalars(
                  select(HabitLog)
                  .where(HabitLog.user_id == user_id)
                  )
            return list(
                  result.all()
                  )

        async def get_by_habit_id(self, habit_id: int) -> list[HabitLog]:
            result = await self.db.scalars(
                  select(HabitLog)
                  .where(HabitLog.habit_id == habit_id)
                  )
            return list(
                  result.all()
                  )

        async def create(self, log_data: HabitLogCreate, user_id:int,habit_id:int) -> HabitLog:
             db_log = HabitLog(**log_data.model_dump(),
                               user_id = user_id,
                               habit_id = habit_id
             )
             self.db.add(db_log)
             await self.db.commit()
             await self.db.refresh(db_log)
             return db_log

        async def update(self, log_id: int, log_update: HabitLogUpdate) -> HabitLog | None:
            log = await self.get_by_id(log_id)
            if log:
                update_data = log_update.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(log, key, value)
                await self.db.commit()
                await self.db.refresh(log)
            return log

        async def delete(self, log_id: int) -> bool:
            log = await self.get_by_id(log_id)
            if log:
                await self.db.delete(log)
                await self.db.commit()
                return True
            return False
