from fastapi import APIRouter

router = APIRouter()

@router.get("/test-users")
async def test_users():
    return {"message": "Users router работает"}