from fastapi import APIRouter

router = APIRouter()

@router.get("/test-auth")
async def test_auth():
    return {"message": "Auth router работает"}