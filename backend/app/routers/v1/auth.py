from app.core.database import get_db
from app.core.security import create_access_token, get_current_user, oauth2_scheme
from app.schemas.user import LoginSchema, UserCreate, UserResponse
from app.services.user_service import UserService
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post("/register", response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    return await user_service.create_user(user_data)

@router.post('/login', status_code=status.HTTP_200_OK)
async def login_user(
    login_data: LoginSchema,
    db: AsyncSession = Depends(get_db)
    ):

    user_service = UserService(db)
    user = await user_service.authenticate_user(login_data.email, login_data.password)

    access_token = create_access_token(subject=user.user_id)

    return {
        "access_token": access_token,
        "user": UserResponse.model_validate(user)
    }

@router.post('/logout')
async def logout(
    current_user:UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)):
    return {"message": "Successfully logged out"}
