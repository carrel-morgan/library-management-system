import pytest
from main import app
from fastapi.testclient import TestClient
import json
import duckdb

from test_data import *

@pytest.fixture()
def test_client():
    return TestClient(app)

@pytest.fixture()
def database():
    con = duckdb.connect()
    yield con

@pytest.fixture(autouse=True)
def create_tables(database):
    database.sql("""
                 CREATE OR REPLACE TABLE books (
                    book_uuid INTEGER,
                    title VARCHAR,
                    author VARCHAR,
                    isbn VARCHAR,
                    quantity INTEGER
                 );
                 """)
    database.sql("""
                CREATE OR REPLACE TABLE patrons (
                    patron_id INTEGER,
                    first_name VARCHAR,
                    last_name VARCHAR,
                    address VARCHAR,
                    phone_number VARCHAR
                 );
                 """)
    database.sql("""
                CREATE OR REPLACE TABLE checkouts (
                    checkout_id INTEGER,
                    book_uuid INTEGER,
                    patron_id INTEGER,
                    checkout_date DATE,
                    due_date DATE,
                    currently_checked_out BOOLEAN,
                    overdue BOOLEAN
                 );
             """)
    yield database
    
@pytest.fixture(autouse=True)
def load_data(database):
    database.sql("COPY books FROM 'project_data/books.csv';")
    database.sql("COPY patrons FROM 'project_data/patrons.csv';")
    database.sql("COPY checkouts FROM 'project_data/checkouts.csv';")

    yield database


class TestEndpoints:
    
    client = TestClient(app) #TODO: Make this a fixture with a generator. 

    def test_initial(self):
        print("Test is working")
        assert True
    
    def test_get_root(self, test_client):
        response = test_client.get("/")
        print("testing response:")
        print(response)
        assert response.status_code == 200
        print(response.json())

    def test_get_available_books(self, test_client):
        response = test_client.get("/api/books")
        response_json = response.json()
        assert response.status_code == 200
        assert response_json["message"] == "placeholder_db_query_results"
        assert response_json["status_code"] == 2001


    def test_checkout_book(self, test_client):
        print(f"testing book dump: {test_book_1.model_dump()}")
        response = test_client.post(
            "/api/checkout",
            json={
                "book_to_checkout": test_book_1.model_dump(), 
                "patron_checking_out": test_patron_1.model_dump()
                }
            )
        response_json = response.json()
        print(f"checkout_response: {response_json}")
        assert response.status_code == 200
        assert response_json["status_code"] == 2001

    def test_return_book(self, test_client):
        response = test_client.post(
            "/api/return",
            json = {
                "book_to_return": test_book_1.model_dump(),
                "patron_returning": test_patron_1.model_dump()
            }
        )
        response_json = response.json()
        print(f"return response: {json.dumps(response_json, indent=4)}")
        assert response.status_code == 200

class TestDatabase:

    def test_query(self):
        duckdb.sql("SELECT 1").show()

    def test_load_book(self, database):
        database.sql("SELECT * FROM books").show()

    def test_load_patrons(self, database):
        database.sql("SELECT * FROM patrons").show()

    def test_load_checkouts(self, database):
        database.sql("SELECT * FROM checkouts").show()