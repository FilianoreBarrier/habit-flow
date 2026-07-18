from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_user, get_password_hash
from app.schemas.user import UserResponse, UserUpdate, ChangePasswordSchema
from app.services.user_service import UserService

router = APIRouter(prefix='/users', tags=['users'])


@router.get("/test", tags=["users"])
async def test_users():
    return {"message": "Users router работает"}


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    """Получить информацию о текущем пользователе"""
    return current_user

@router.patch('/me')
def update_user(
    user_update: UserUpdate,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
    ):
    user_service = UserService(db)
    return user_service.update_user(current_user.user_id, user_update)

@router.post('/me/change-password',response_model=UserResponse, status_code=status.HTTP_200_OK)
def change_user_password(
    change_data: ChangePasswordSchema,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
    ):
    user_service = UserService(db)
    return user_service.change_password(current_user.user_id, change_data.old_password, change_data.new_password)

@router.post('/me/deactivate', response_model=UserResponse, status_code=status.HTTP_200_OK)
def deactivate_user(db: AsyncSession = Depends(get_db),current_user:UserResponse = Depends(get_current_user)):
    user_service = UserService(db)
    return user_service.deactivate_user(current_user.user_id)

@router.get('/{user_id}',response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    return user_service.get_by_id(user_id)
