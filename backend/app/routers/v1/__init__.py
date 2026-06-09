from .auth import router as auth_router
from .habits import router as habits_router
from .users import router as users_router

__all__ = ["auth_router", "habits_router", "users_router"]
