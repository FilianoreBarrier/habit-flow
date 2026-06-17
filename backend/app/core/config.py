from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Habit Flow"
    debug: bool = True
    database_url: str = "sqlite:///./habitflow.db"
    # CORS
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    # JWT настройки
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore"   # ← Это важно!


settings = Settings()