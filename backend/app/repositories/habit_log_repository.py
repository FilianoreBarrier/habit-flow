from app.models.habit_log import HabitLog
from app.schemas.habit_log import HabitLogCreate, HabitLogUpdate
from sqlalchemy import select
from sqlalchemy.orm import Session


class HabitLogRepository:
        def __init__(self,db:Session):
            self.db = db

        def get_by_id(self,log_id:int) -> HabitLog| None:
              return self.db.get(HabitLog, log_id)
        
        def get_by_completed(self, completed:bool) -> HabitLog| None:
              return self.db.scalar(select(HabitLog).where(HabitLog.completed == completed))
        
        def get_by_user_id(self, user_id: int) -> list[HabitLog]:
            return list(
                  self.db.scalars(
                  select(HabitLog)
                  .where(HabitLog.user_id == user_id)
                  ).all()
                  )
        def get_by_habit_id(self, habit_id: int) -> list[HabitLog]:
            return list(
                  self.db.scalars(
                  select(HabitLog)
                  .where(HabitLog.habit_id == habit_id)
                  ).all()
                  )
        def create(self, log_data: HabitLogCreate, user_id:int,habit_id:int) -> HabitLog:
             db_log = HabitLog(**log_data.model_dump(),
                               user_id = user_id,
                               habit_id = habit_id
             )
             self.db.add(db_log)
             self.db.commit()
             self.db.refresh(db_log)
             return db_log
        
        def update(self, log_id: int, log_update: HabitLogUpdate) -> HabitLog | None:
            log = self.get_by_id(log_id)
            if log:
                update_data = log_update.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(log, key, value)
                self.db.commit()
                self.db.refresh(log)
            return log
        
        def delete(self, log_id: int) -> bool:
            log = self.get_by_id(log_id)
            if log:
                self.db.delete(log)
                self.db.commit()
                return True
            return False