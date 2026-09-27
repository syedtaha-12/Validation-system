import sqlite3

conn = sqlite3.connect("banking_qa.db")
cur = conn.cursor()

# Rebuild table each run for QA repeatability
cur.execute("DROP TABLE IF EXISTS account_summary;")

# Create account-level report from validated data
cur.execute("""
CREATE TABLE account_summary AS
SELECT
    account_id,
    COUNT(*) AS transaction_count,
    SUM(amount_cents) AS total_amount_cents
FROM transactions_validated
GROUP BY account_id
ORDER BY account_id;
""")

conn.commit()

# Quick verification (first few rows only)
cur.execute("SELECT COUNT(*) FROM account_summary;")
print("account_summary rows:", cur.fetchone()[0])

cur.execute("SELECT * FROM account_summary LIMIT 5;")
for r in cur.fetchall():
    print(" ", r)

conn.close()
