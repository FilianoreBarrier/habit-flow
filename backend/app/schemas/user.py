from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=20, description="Unique username")
    email: EmailStr= Field(description="User email for authorization")
    full_name: Optional[str] = Field(default=None,max_length=50,description='User full name')

class UserCreate(UserBase):
    password: str = Field(min_length=8
, description='User password for authorization')

class UserResponse(UserBase):
    user_id: int = Field(description="Unique user identifier")
    is_active: bool = Field(description='Shows user activity ')
    created_at: datetime
    model_config = {"from_attributes":True}


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    email: Optional[EmailStr] = None
    hashed_password: Optional[str] = None

class LoginSchema(BaseModel):
    email: EmailStr = Field(description="Email for login")
    password: str = Field(description="Password for login")

class ChangePasswordSchema(BaseModel):
    old_password: str = Field(min_length=8)
    new_password: str = Field(min_length=8)
