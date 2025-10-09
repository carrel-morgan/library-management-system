from main import LMSResponse
from main import LMSBook
from main import LMSPatron

test_book_1 = LMSBook(
    book_uuid = 1234,
    title = "Pride and Prejudice",
    author = "Steve",
    isbn = "AR987654321",
    quantity = 10
)

test_patron_1 = LMSPatron(
    id = 1337,
    first_name="Jane",
    last_name="Doe",
    address="5678 Street Rd, San Francisco, CA, 99998",
    phone_number="1-222-444-6666"
)