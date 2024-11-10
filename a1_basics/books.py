import uvicorn
from fastapi import FastAPI, HTTPException, Path, Query
from starlette import status

from a1_basics.models import Book, BookRequest

app = FastAPI()

BOOKS = [
    Book(
        1,
        "To Kill a Mockingbird",
        "Harper Lee",
        "A classic novel of racism and injustice in the Deep South.",
        5,
        1960,
    ),
    Book(
        2,
        "1984",
        "George Orwell",
        "A dystopian novel depicting a totalitarian regime and Big Brother surveillance.",
        5,
        1949,
    ),
    Book(
        3,
        "The Great Gatsby",
        "F. Scott Fitzgerald",
        "A tragic love story set in the Jazz Age.",
        4,
        1925,
    ),
    Book(
        4,
        "Moby Dick",
        "Herman Melville",
        "A story of obsession and revenge on the high seas.",
        3,
        1851,
    ),
    Book(
        5,
        "Pride and Prejudice",
        "Jane Austen",
        "A witty romance exploring class and society in England.",
        5,
        1813,
    ),
    Book(
        6,
        "The Catcher in the Rye",
        "J.D. Salinger",
        "A tale of teenage rebellion and self-discovery.",
        4,
        1951,
    ),
    Book(
        7,
        "The Hobbit",
        "J.R.R. Tolkien",
        "A fantasy adventure preceding the events of The Lord of the Rings.",
        5,
        1937,
    ),
    Book(
        8,
        "The Road",
        "Cormac McCarthy",
        "A bleak post-apocalyptic journey of a father and son.",
        4,
        2006,
    ),
    Book(
        9,
        "Sapiens: A Brief History of Humankind",
        "Yuval Noah Harari",
        "A thought-provoking exploration of human history and culture.",
        5,
        2011,
    ),
    Book(
        10,
        "Becoming",
        "Michelle Obama",
        "A memoir detailing the life and experiences of the former First Lady.",
        4,
        2018,
    ),
]


# `status.HTTP_200_OK` indicates that the request was successful
@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


# Endpoint to retrieve a specific book by ID
# `Path` validates that `book_id` is a positive integer (`gt=0`)
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.book_id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item not found")


# Endpoint to retrieve books filtered by rating using a query parameter
# `Query` limits `book_rating` between 1 and 5
@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_books_by_publish_date(published_date: int = Query(gt=1800, lt=2100)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


# This endpoint uses a Pydantic model (`BookRequest`) to define and validate the structure of the incoming data.
# `BookRequest` helps ensure that the data sent by the client meets the required structure and constraints.
# For example, it checks that the title has at least 3 characters, the rating is between 1 and 5, and other fields meet their specified rules.
# Using `BookRequest` also enables auto-generated API documentation, showing required fields and example data.
@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.book_id = 1 if len(BOOKS) == 0 else BOOKS[-1].book_id + 1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].book_id == book.book_id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].book_id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")


if __name__ == "__main__":
    uvicorn.run("books:app", host="localhost", port=5001, reload=True)
