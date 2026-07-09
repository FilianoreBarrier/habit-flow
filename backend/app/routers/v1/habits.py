from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.habit import HabitUpdate, HabitResponse,HabitCreate
from app.schemas.user import UserResponse
from app.services.habit_service import HabitService
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/habits", tags=["habits"])

@router.get("/test-habits")
async def test_habits(current_user: UserResponse = Depends(get_current_user)):
    return {"message": "Habits router работает", "current_user_id": current_user.id}

@router.patch("/{habit_id}", response_model=HabitResponse)
async def update_habit(
    habit_id: int,
    habit_update: HabitUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)

):
    habit_service = HabitService(db)
    return habit_service.update_habit(habit_id, habit_update, current_user.id)

@router.get("/", response_model=list[HabitResponse])
async def get_user_habits(db: Session = Depends(get_db),current_user: UserResponse = Depends(get_current_user)):
    """Получить все привычки текущего пользователя"""
    habit_service = HabitService(db)
    return habit_service.get_user_habits(current_user.id)

@router.post("/",response_model=HabitResponse, status_code=201)
async def create_habit(habit_data: HabitCreate, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    """Создать новую привычку"""
    habit_service = HabitService(db)
    return habit_service.create_habit(habit_data,current_user.id)

@router.get("/{habit_id}", response_model=HabitResponse)
async def get_habit(habit_id: int, current_user: UserResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    """Получить одну привычку"""
    habit_service = HabitService(db)
    return habit_service.get_habit_by_id(habit_id, current_user.id)

@router.delete("/{habit_id}")
async def delete_habit(habit_id: int, current_user: UserResponse = Depends(get_current_user), db: Session = Depends(get_db)):
    """Удалить привычку"""
    habit_service = HabitService(db)
    return habit_service.delete_habit(habit_id, current_user.id)
