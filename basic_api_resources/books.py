from fastapi import Body, FastAPI, HTTPException

app = FastAPI(
    title="Books API",
    description="API for managing books, authors, and categories",
    version="1.0.0"
)


BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

# 📚 --- BOOKS SECTION ---

@app.get("/books", tags=["📚 Books"], summary="Read All Books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_title}", tags=["📚 Books"], summary="Read Book by Title")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books/create_book", tags=["📚 Books"], summary="Create New Book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books/update_book", tags=["📚 Books"], summary="Update Book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book


@app.delete("/books/delete_book/{book_title}", tags=["📚 Books"], summary="Delete Book by Title")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break


# ✍️ --- AUTHORS SECTION ---
# Get all books from a specific author using path or query parameters
@app.get("/books/byauthor/", tags=["✍️ Authors"], summary="Read Books by Author (Path)")
async def read_books_by_author_path(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)

    return books_to_return


@app.get("/books/{book_author}/", tags=["✍️ Authors"], summary="Read Author Category by Query")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
                book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


# 🧠 --- CATEGORIES SECTION ---
@app.get("/books/", tags=["🧠 Category"], summary="Read Book by Category")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return



