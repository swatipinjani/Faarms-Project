# build a schema using pydantic
from pydantic import BaseModel
from typing import List

class Book(BaseModel):
    book_name: str
    description: str
    image_link: str

    class Config:
        orm_mode = True


class Customer(BaseModel):
    name: str
    password: str
    email: str

    class Config:
        orm_mode = True

class FavoriteBooks(BaseModel):
    customer_id: int
    favourite_books_list: str

    class Config:
        orm_mode = True

