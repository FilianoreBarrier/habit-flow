from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.habit_log import HabitLogCreate, HabitLogResponse
from app.schemas.user import UserResponse
from app.services.habit_log_service import HabitLogService

router = APIRouter(prefix="/habits", tags=["habit_logs"])


@router.post("/{habit_id}/log", response_model=HabitLogResponse)
async def log_habit(habit_id: int,
                    log_data: HabitLogCreate,
                    current_user: UserResponse = Depends(get_current_user),
                    db: Session = Depends(get_db)):

    """Отметить выполнение привычки (лог)"""
    log_service = HabitLogService(db)
    return log_service.create_log(log_data,habit_id,current_user.user_id)


@router.get("/{habit_id}/logs", response_model=list[HabitLogResponse])
async def get_habit_logs(
    habit_id: int,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    log_service = HabitLogService(db)
    return log_service.get_logs_by_habit(habit_id,current_user.user_id)


@router.get("/logs", response_model=list[HabitLogResponse])
async def get_user_logs(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Получить все логи текущего пользователя"""
    log_service = HabitLogService(db)
    return log_service.get_logs_by_user(current_user.user_id)
