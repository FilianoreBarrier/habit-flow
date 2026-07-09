from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.database import init_db

# Импорт роутеров
from routers.v1 import auth_router, users_router, habits_router, habit_logs_router

app = FastAPI(
    title="HabitFlow",
    description="Приложение для трекинга привычек",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(users_router, prefix="/api/v1", tags=["users"])
app.include_router(habits_router, prefix="/api/v1", tags=["habits"])
app.include_router(habit_logs_router, prefix="/api/v1", tags=["habit_logs"])


@app.on_event("startup")
async def startup_event():
    init_db()
    print("✅ HabitFlow запущен. База данных инициализирована.")


@app.get("/")
async def root():
    return {"message": "HabitFlow API работает!", "docs": "/docs"}
