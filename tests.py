import pytest
from main import app, setup_database
from fastapi.testclient import TestClient
import json
import duckdb
from database_definition_language import (
    create_books_table_sql,
    create_patrons_table_sql,
    create_checkouts_table,
    copy_books_from_csv_sql,
    copy_patrons_from_csv_sql,
    copy_checkouts_from_csv_sql
)
from test_data import *
from validation_and_reconciliation import validate_available_books

@pytest.fixture()
def database():
    con = duckdb.connect()
    yield con

@pytest.fixture(autouse=True)
def create_tables(database):
    database.sql(create_books_table_sql)
    database.sql(create_patrons_table_sql)
    database.sql(create_checkouts_table)
    yield database
    
@pytest.fixture(autouse=True)
def load_data(database):
    database.sql(copy_books_from_csv_sql)
    database.sql(copy_patrons_from_csv_sql)
    database.sql(copy_checkouts_from_csv_sql)

    yield database

@pytest.fixture()
def test_client(database):
    with TestClient(app) as client:
        yield client

class TestEndpoints:
    
    client = TestClient(app) #TODO: Make this a fixture with a generator. 
    # setup_database(client)

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
        print(f"get_available_books_response: \n {json.dumps(response.json(), indent=4)}")
        assert response.status_code == 200
        # assert response_json["message"] == "placeholder_db_query_results"
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

    def test_validate_available_books(self, database):
        validate_available_books(database)