import duckdb
import polars

def validate_available_books(lms_connection: duckdb.DuckDBPyConnection):
    validation_results = lms_connection.sql("""
                        SELECT books.book_uuid, num_available, quantity as total_in_inventory, total_checked_out
                        FROM books
                        LEFT JOIN (
                            SELECT book_uuid, COUNT(book_uuid) as total_checked_out
                            FROM checkouts     
                            WHERE currently_checked_out is True
                            GROUP BY book_uuid
                       ) as checked_out_books
                       ON books.book_uuid == checked_out_books.book_uuid
                       """).pl()
    print(validation_results)
    # total_available = polars.col("total_in_inventory") - polars.col("total_checked_out")
    total_available = validation_results.select(
        polars.all(),
        (polars.col("total_in_inventory") - polars.col("total_checked_out")).alias("calculated_total_available"),
        (polars.col("num_available") - (
                polars.col("total_in_inventory") - polars.col("total_checked_out")
                )
            ).alias("num_mismatch")
    )
    inventory_checkout_mismatch = total_available.select(
        polars.col("book_uuid"),
        polars.col("num_available"),
        polars.col("total_checked_out"),
        polars.col("num_mismatch")
    ).filter(
        polars.col("num_mismatch") > 0
    )
    print(inventory_checkout_mismatch)
    return inventory_checkout_mismatch

def reconcile_checkouts_and_inventory(lms_connection: duckdb.DuckDBPyConnection, books_to_reconcile: polars.DataFrame):
    print("Reconciling checkouts and inventory...")
    #TODO: Implement reconciliation. 