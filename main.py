from fastapi import FastAPI
from pydantic import BaseModel
from database_definition_language import (
    create_books_table_sql,
    create_patrons_table_sql,
    create_checkouts_table,
    copy_books_from_csv_sql,
    copy_patrons_from_csv_sql,
    copy_checkouts_from_csv_sql
)
import duckdb

app = FastAPI()

conn = duckdb.connect()

#Ideally this should be a class, but at this point that's going to take more time than I have to dedicate to this. 
def setup_database(lms_connection: duckdb.DuckDBPyConnection):
    lms_connection.sql(create_books_table_sql)
    lms_connection.sql(create_patrons_table_sql)
    lms_connection.sql(create_checkouts_table)
    lms_connection.sql(copy_books_from_csv_sql)
    lms_connection.sql(copy_patrons_from_csv_sql)
    lms_connection.sql(copy_checkouts_from_csv_sql)
    return lms_connection

class LMSResponse(BaseModel):
    """Skeleton class for an (L)ibarary (M)anagement (S)ystem response"""
    response_type: str # Book, transaction, customer, etc.
    message: str
    success_code: int
    # TODO: Fill out skeleton into actual response

class LMSBook(BaseModel):
    """Skeleton class for a book, to correspond to the database model"""
    book_uuid: int
    title: str
    author: str
    isbn: str
    quantity: int
    num_available: int

class LMSPatron(BaseModel):
    """Skeleton class for a library patron"""
    id: int #TODO: Maybe make the id a hash. 
    first_name: str
    last_name: str
    address: str # Break these into multipart address? Or have it be a contact class. 
    phone_number: str

class LMSTransaction(BaseModel):
    """Skeleton class for a library system transaction(AKA a checkout)"""
    checkout_id: int
    book_uuid: int
    patron_id: int
    checkout_date: str
    due_date: str
    currently_checked_out: bool
    overdue: bool

setup_database(conn)

@app.get("/")
async def root():
    return {"message": "Hello, User."}

@app.get("/api/books")
async def get_available_books():
    db_query = """
    SELECT *
    FROM books
    WHERE num_available > 0
    ORDER BY title
    """
    db_query_results = conn.sql(db_query).fetchall()
    #TODO: Serialize these results into an object. 
    print("printing db query results: ")
    print(db_query_results)
    return {"message": db_query_results,
            "status_code": 2001}

@app.post("/api/checkout")
async def checkout_book(book_to_checkout: LMSBook, patron_checking_out: LMSPatron):
    return {"message": "Checkout Success! Or Checkout Failure! We're not sure yet. This feature under development.",
            "status_code": 2001}

@app.post("/api/return")
async def return_book(book_to_return: LMSBook, patron_returning: LMSPatron):
    return {"message": "You have attempted to return a book. It may or may not have worked.",
            "status_code": 2001}

def main(): 
    conn = duckdb.connect()
    setup_database(conn)
    
    