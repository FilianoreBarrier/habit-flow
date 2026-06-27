from typing import List

from app.core.security import get_password_hash
from app.repositories.habit_repository import HabitRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


class UserService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)
        self.habit_repository = HabitRepository(db)

    def create_user(self, user_data: UserCreate) -> UserResponse:
        if self.user_repository.get_by_email(user_data.email):
            raise HTTPException(
                 status_code=status.HTTP_409_CONFLICT,
                 detail='The email is already taken.'
             )  # ошибка "email уже занят"
        if self.user_repository.get_by_username(user_data.username):
            raise HTTPException(
                 status_code=status.HTTP_409_CONFLICT,
                 detail='The username is already taken'
             )  # ошибка "username уже занят"
        hashed_password = get_password_hash(user_data.password)
        user = self.user_repository.create(user_data, hashed_password)
        return UserResponse.model_validate(user)

#     def get_all_products (self) -> ProductListResponse:
#         products = self.product_repository.get_all()
#         products_response=[ProductResponse.model_validate(prod) for prod in products]
#         return ProductListResponse(products = products_response, total=len(products_response))

#     def get_product_by_id(self, product_id:int) -> ProductResponse:
#         product = self.product_repository.get_by_id(product_id)
#         if not product:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f'Product with id {product_id} not found'
#             )
#         return ProductResponse.model_validate(product)

#     def get_product_by_category(self, category_id:int) -> ProductListResponse:
#         category = self.category_repository.get_by_id(category_id)
#         if not category:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail= f'Category with id {category_id} not found'
#             )
#         products = self.product_repository.get_by_category(category_id)
#         products_response = [ProductResponse.model_validate(prod) for prod in products]
#         return ProductListResponse(products=products_response, total = len(products_response))

#     def create_product(self, product_data: ProductCreate) -> ProductResponse:
#         category = self.category_repository.get_by_id(product_data.category_id)
#         if not category:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f'Category with id {product_data.category_id} does not exist'
#             )
#         product = self.product_repository.create(product_data)
#         return ProductResponse.model_validate(product)
