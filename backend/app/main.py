from app.core.config import settings
from app.core.database import init_db
from app.routers.v1 import auth, habits, users
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="HabitFlow",
    description="Приложение для трекинга привычек",
    version="1.0.0"
)

# CORS (чтобы фронтенд мог обращаться к бэкенду)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(habits.router, prefix="/api/v1", tags=["habits"])


@app.on_event("startup")
async def startup_event():
    init_db()          # Создаёт таблицы в базе данных при запуске
    print(" HabitFlow запущен. База данных инициализирована.")


@app.get("/")
async def root():
    return {
        "message": "HabitFlow API работает!",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)