from fastapi import HTTPException, status


def raise_user_not_found(user_id: int):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {user_id} not found."
    )

