import sqlite3
import csv
from decimal import Decimal


def to_cents(value):
    """Convert an amount string like '125.50' to integer cents; blank -> None."""
    value = value.strip()
    if not value:
        return None
    return int((Decimal(value) * 100).to_integral_value())


# 1. Create / connect to the SQLite database
conn = sqlite3.connect("banking_qa.db")
cursor = conn.cursor()

# 2. Recreate the raw staging table on every run.
# Amounts are stored as integer cents so totals add up exactly at any volume.
cursor.execute("DROP TABLE IF EXISTS transactions_raw")
cursor.execute("""
CREATE TABLE transactions_raw (
    transaction_id INTEGER,
    account_id TEXT,
    amount_cents INTEGER,
    date TEXT
)
""")

# 3. Bulk-load data from CSV into the database
with open("transactions.csv", "r", newline="") as file:
    reader = csv.DictReader(file)
    cursor.executemany(
        "INSERT INTO transactions_raw VALUES (?, ?, ?, ?)",
        (
            (int(row["transaction_id"]), row["account_id"], to_cents(row["amount"]), row["date"])
            for row in reader
        ),
    )

# Speeds up the duplicate check and deduplication in the validated view.
cursor.execute("CREATE INDEX idx_raw_transaction_id ON transactions_raw (transaction_id)")

# 4. Save changes and close the database connection
conn.commit()

cursor.execute("SELECT COUNT(*) FROM transactions_raw")
print(f"Database created and {cursor.fetchone()[0]} rows loaded successfully.")

conn.close()
