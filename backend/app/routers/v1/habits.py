from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.habit import HabitUpdate
from app.schemas.user import UserResponse
from app.services.habit_service import HabitService
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/test-habits")
async def test_habits(current_user: UserResponse = Depends(get_current_user)):
    return {"message": "Habits router работает", "current_user_id": current_user.id}

@router.put("/{habit_id}")
async def update_habit(
    habit_id: int,
    habit_update: HabitUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    habit_service = HabitService(db)
    return habit_service.update_habit(habit_id, habit_update, current_user.id)