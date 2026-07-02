from fastapi import HTTPException, status


def raise_user_not_found(user_id: int):
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = f"User with id {user_id} not found."
    )

def raise_habit_not_found(habit_id: int):
    raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Habit with id {habit_id} not found."

            )
