import sqlite3

conn = sqlite3.connect("banking_qa.db")
cur = conn.cursor()

# 1) Re-create the reporting table each run (makes it repeatable for QA)
cur.execute("DROP TABLE IF EXISTS daily_summary;")

# 2) Create daily summary report from VALIDATED data (clean source)
cur.execute("""
CREATE TABLE daily_summary AS
SELECT
    date,
    COUNT(*) AS transaction_count,
    SUM(amount_cents) AS total_amount_cents
FROM transactions_validated
GROUP BY date
ORDER BY date;
""")

conn.commit()

# 3) Quick verification output (first few rows only)
cur.execute("SELECT COUNT(*) FROM daily_summary;")
print("daily_summary rows:", cur.fetchone()[0])

cur.execute("SELECT * FROM daily_summary LIMIT 5;")
for r in cur.fetchall():
    print(" ", r)

conn.close()
