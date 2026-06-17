# Импорты внутри пакета app
from core.config import settings
from core.database import init_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.v1 import auth, habits, users

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

app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(habits.router, prefix="/api/v1", tags=["habits"])


@app.on_event("startup")
async def startup_event():
    init_db()
    print("✅ HabitFlow запущен. База данных инициализирована.")


@app.get("/")
async def root():
    return {"message": "HabitFlow API работает!", "docs": "/docs"}