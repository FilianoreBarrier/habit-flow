from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/test", tags=["users"])
async def test_users():
    return {"message": "Users router работает"}


# Пример будущего эндпоинта
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.create_user(user_data)