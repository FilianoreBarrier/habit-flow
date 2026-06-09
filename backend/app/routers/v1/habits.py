from fastapi import APIRouter

router = APIRouter()

@router.get("/test-habits")
async def test_habits():
    return {"message": "Habits router работает"}