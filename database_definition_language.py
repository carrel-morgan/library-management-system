create_books_table_sql = """
                 CREATE OR REPLACE TABLE books (
                    book_uuid INTEGER,
                    title VARCHAR,
                    author VARCHAR,
                    isbn VARCHAR,
                    quantity INTEGER,
                    num_available INTEGER
                 );
                 """

create_patrons_table_sql = """
                CREATE OR REPLACE TABLE patrons (
                    patron_id INTEGER,
                    first_name VARCHAR,
                    last_name VARCHAR,
                    address VARCHAR,
                    phone_number VARCHAR
                 );
                 """

create_checkouts_table = """
                CREATE OR REPLACE TABLE checkouts (
                    checkout_id INTEGER,
                    book_uuid INTEGER,
                    patron_id INTEGER,
                    checkout_date DATE,
                    due_date DATE,
                    currently_checked_out BOOLEAN,
                    overdue BOOLEAN
                 );
             """

#TODO: Dynamically generate paths to source data using Path library
copy_books_from_csv_sql = "COPY books FROM 'project_data/books.csv';"
copy_patrons_from_csv_sql = "COPY patrons FROM 'project_data/patrons.csv';"
copy_checkouts_from_csv_sql = "COPY checkouts FROM 'project_data/checkouts.csv';"