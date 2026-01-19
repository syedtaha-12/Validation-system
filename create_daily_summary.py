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
    SUM(amount) AS total_amount
FROM transactions_validated
GROUP BY date;
""")

conn.commit()

# 3) Quick verification output
cur.execute("SELECT * FROM daily_summary;")
rows = cur.fetchall()

print("daily_summary rows:")
for r in rows:
    print(r)

conn.close()
