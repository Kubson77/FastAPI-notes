"""A basic FastAPI application demonstrating how to build and interact with RESTful APIs."""

import uvicorn
from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {
        "title": "A Brief History of Time",
        "author": "Stephen Hawking",
        "category": "science",
    },
    {"title": "The Selfish Gene", "author": "Richard Dawkins", "category": "science"},
    {
        "title": "Sapiens: A Brief History of Humankind",
        "author": "Yuval Noah Harari",
        "category": "history",
    },
    {
        "title": "Guns, Germs, and Steel",
        "author": "Jared Diamond",
        "category": "history",
    },
    {
        "title": "The Art of Statistics",
        "author": "David Spiegelhalter",
        "category": "math",
    },
    {
        "title": "Mathematics for the Nonmathematician",
        "author": "Morris Kline",
        "category": "math",
    },
    {"title": "Cosmos", "author": "Carl Sagan", "category": "science"},
    {
        "title": "A People’s History of the United States",
        "author": "Howard Zinn",
        "category": "history",
    },
    {
        "title": "The Code Book: The Science of Secrecy",
        "author": "Simon Singh",
        "category": "science",
    },
    {
        "title": "Introduction to the Theory of Computation",
        "author": "Michael Sipser",
        "category": "math",
    },
]


@app.get("/books")
async def read_all_books():
    return BOOKS


# Endpoint to retrieve a specific book by its title, provided as a path parameter
# Use URL encoding for spaces when testing in a browser, e.g. localhost:5001/books/the%20selfish%20gene
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book


# Endpoint to retrieve books by category, specified as a query parameter, e.g. localhost:5001/books/?category=math
@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


# Endpoint to retrieve books by author, specified as a query parameter
# IMPORTANT: This endpoint must be defined before `/books/{book_author}/` to avoid conflicts.
# If `/books/{book_author}/` is placed before, it will capture requests for specific authors
# and bypass the `/books/byauthor/` endpoint, resulting in missing 'category' data.
@app.get("/books/byauthor/")
async def read_books_by_author_path(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == author.casefold():
            books_to_return.append(book)

    return books_to_return


# Endpoint to retrieve books by both author (path parameter) and category (query parameter)
@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if (
            book.get("author").casefold() == book_author.casefold()
            and book.get("category").casefold() == category.casefold()
        ):
            books_to_return.append(book)

    return books_to_return


# Endpoint to add a new book to the list using POST
@app.post("/books/create_book")
async def create_book(new_book: dict = Body()):
    BOOKS.append(new_book)


# Endpoint to update an existing book's information using PUT
@app.put("/books/update_book")
async def update_book(updated_book: dict = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book


# Endpoint to delete a book from the list using DELETE
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            break


if __name__ == "__main__":
    uvicorn.run("example:app", host="localhost", port=5001, reload=True)
