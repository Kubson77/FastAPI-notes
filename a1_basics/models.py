from typing import Optional

from pydantic import BaseModel, Field


class Book:
    def __init__(self, book_id, title, author, description, rating, published_date):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    book_id: Optional[int] = Field(
        description="ID is not needed on create", default=None
    )
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1800, lt=2100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "An author",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2020,
            }
        }
    }

    # Old version of configuration:

    # class Config:
    #     json_schema_extra = {
    #         'example': {
    #             'title': 'A new book',
    #             'author': 'An author',
    #             'description': 'A new description of a book',
    #             'rating': 5,
    #             'published_date': 2020
    #         }
    #     }
