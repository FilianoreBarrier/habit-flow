from app.core.database import get_db
from app.core.security import create_access_token, get_current_user
from app.schemas.user import LoginSchema, UserCreate, UserResponse
from app.services.user_service import UserService
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post("/register", response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.create_user(user_data)

@router.post('/login', status_code=status.HTTP_200_OK)
def login_user(
    login_data: LoginSchema,
    db: Session = Depends(get_db)
    ):

    user_service = UserService(db)
    user = user_service.authenticate_user(login_data.email, login_data.password)

    access_token = create_access_token(subject=user.id)

    return {
        "access_token": access_token,
        "user": UserResponse.model_validate(user)
    }

@router.post('/logout')
def logout(current_user:UserResponse = Depends(get_current_user)):
    return {"message": "Successfully logged out"}
