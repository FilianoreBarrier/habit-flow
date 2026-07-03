from app.core.exceptions import (raise_habit_log_not_found,
                                 raise_habit_not_found, raise_user_not_found)
from app.repositories.habit_log_repository import HabitLogRepository
from app.repositories.habit_repository import HabitRepository
from app.repositories.user_repository import UserRepository
from app.schemas.habit_log import (HabitLogCreate, HabitLogResponse,
                                   HabitLogUpdate)
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


class HabitLogService:
    def __init__(self, db: Session):
        self.habit_log_repository = HabitLogRepository(db)
        self.habit_repository = HabitRepository(db)
        self.user_repository = UserRepository(db)

    def create_log(self, log_data: HabitLogCreate, habit_id: int, user_id: int) -> HabitLogResponse:
        if not self.user_repository.get_by_id(user_id):
            raise_user_not_found(user_id)
        habit = self.habit_repository.get_by_id(habit_id)
        if not habit:
            raise_habit_not_found(habit_id)

        if habit.user_id != user_id: # type: ignore[attr-defined]
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail ='You can only create logs for your own habits.'
            )
        
        log = self.habit_log_repository.create(log_data, user_id, habit_id)

        return HabitLogResponse.model_validate(log)

    def get_logs_by_habit(self, habit_id: int, user_id: int) -> list[HabitLogResponse]:
        if not self.user_repository.get_by_id(user_id):
            raise_user_not_found(user_id)

        habit = self.habit_repository.get_by_id(habit_id)
        if not habit:
            raise_habit_not_found(habit_id)

        if habit.user_id != user_id: # type: ignore[attr-defined]
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail ='You can only view logs of your own habits.'
            )


        logs = self.habit_log_repository.get_by_habit_id(habit_id) 
        return [HabitLogResponse.model_validate(log) for log in logs]

    def get_logs_by_user(self, user_id: int) -> list[HabitLogResponse]:

        if not self.user_repository.get_by_id(user_id):
            raise_user_not_found(user_id)

        logs = self.habit_log_repository.get_by_user_id(user_id) 
        return [HabitLogResponse.model_validate(log) for log in logs]
        

    def get_log_by_id(self, log_id: int, user_id: int) -> HabitLogResponse:
        log = self.habit_log_repository.get_by_id(log_id)
        if not log or log.user_id != user_id:# type: ignore[attr-defined]
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Habit log not found or you dont have access to it '
            )
        return HabitLogResponse.model_validate(log)

    def update_log(self, log_id: int, log_update: HabitLogUpdate, user_id: int) -> HabitLogResponse:
        
        log = self.habit_log_repository.get_by_id(log_id)
        
        if not log:
            raise_habit_log_not_found(log_id)    
        
        if log.user_id != user_id: # type: ignore[attr-defined]
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You can only update your own habit logs! '
            )
        
        updated_log = self.habit_log_repository.update(log_id, log_update)
        return HabitLogResponse.model_validate(updated_log)

    def delete_log(self, log_id: int, user_id: int) -> bool:

        log = self.habit_log_repository.get_by_id(log_id)

        if not log:
            raise_habit_log_not_found(log_id)    

        if log.user_id != user_id: # type: ignore[attr-defined]
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You can only delete your own habit logs! '
            )
        
        self.habit_log_repository.delete(log_id)
        return True