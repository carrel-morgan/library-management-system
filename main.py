from fastapi import FastAPI
import msgspec

app = FastAPI()


class LMSResponse(msgspec.Struct):
    """Skeleton class for an (L)ibarary (M)anagement (S)ystem response"""
    response_type: str # Book, transaction, customer, etc.
    message: str
    success_code: int
    # TODO: Fill out skeleton into actual response

class LMSBook(msgspec.Struct):
    """Skeleton class for a book, to correspond to the database model"""
    book_uuid: int
    title: str
    author: str
    isbn: str
    quantity: int

class Patron(msgspec.Struct):
    """Skeleton class for a library patron"""
    id: int #TODO: Maybe make the id a hash. 
    first_name: str
    last_name: str
    address: str # Break these into multipart address? Or have it be a contact class. 
    phone_number: str

@app.get("/")
async def root():
    return {"message": "Hello, User."}

@app.get("/api/books")
async def get_available_books():
    db_query = """
    SELECT *
    FROM books
    ORDER BY title
    """
    db_query_results = "" # TODO: Implement a simple database
    return {"message": db_query_results}

@app.post("/api/checkout")
async def checkout_book(book_to_checkout: LMSBook, customer_checking_out: Patron):
    return {"message": "Checkout Success! Or Checkout Failure! We're not sure yet. This feature under development."}

@app.post("/api/return")
async def checkout_book(book_to_return: LMSBook):
    return {"message": "You have attempted to return a book. It may or may not have worked."}