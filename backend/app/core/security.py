from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Union
import bcrypt
from app.core.config import settings
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserResponse
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.token_repository import TokenRepository

# ==================== Security Config ====================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Ссылка, куда FastAPI будет отправлять пользователя для логина
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# ==================== Password Hashing ====================
def get_password_hash(password: str) -> str:
    """Хэширует пароль с помощью bcrypt"""
    password_bytes = password[:72].encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль"""
    plain_bytes = plain_password[:72].encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_bytes, hashed_bytes)


# ==================== JWT Operations ====================

def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Создаёт JWT access token"""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    # Payload токена. Поле 'sub' обязательно должно содержать ID пользователя
    to_encode = {"exp": expire, "sub": str(subject)}

    # Создаём JWT токен через PyJWT
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Декодирует JWT токен и возвращает payload или None при ошибке"""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return payload
    except InvalidTokenError:
        return None


# ==================== FastAPI Dependencies ====================

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_repo = TokenRepository(db)
    if await token_repo.is_token_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is blacklisted. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 2. Твой старый код (декодирование JWT и поиск юзера) ...
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    # Получаем ID пользователя из поля 'sub'
    user_id: Optional[str] = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    # Ищем пользователя в базе данных через репозиторий
    user = await UserRepository(db).get_by_id(int(user_id))
    if user is None:
        raise credentials_exception

    # Возвращаем валидированную Pydantic-модель пользователя
    return UserResponse.model_validate(user)
