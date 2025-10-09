import pytest
from main import app
from fastapi.testclient import TestClient
import json

from test_data import *

@pytest.fixture()
def test_client():
    return TestClient(app)

class TestMain:
    
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