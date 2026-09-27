import sqlite3

conn = sqlite3.connect("banking_qa.db")
cur = conn.cursor()

cur.execute("DROP VIEW IF EXISTS transactions_validated;")

cur.execute("""
CREATE VIEW transactions_validated AS
SELECT transaction_id, account_id, amount_cents, date
FROM transactions_raw
WHERE amount_cents IS NOT NULL
  AND amount_cents >= 0
  AND rowid IN (
      SELECT MIN(rowid)
      FROM transactions_raw
      GROUP BY transaction_id
  );
""")
conn.commit()

cur.execute("""
SELECT transaction_id, COUNT(*)
FROM transactions_raw
GROUP BY transaction_id
HAVING COUNT(*) > 1;
""")
dupes = cur.fetchall()
print(f"Duplicate transaction IDs: {len(dupes)}", dupes[:10], "..." if len(dupes) > 10 else "")

cur.execute("SELECT COUNT(*) FROM transactions_raw WHERE amount_cents IS NULL;")
print("Missing amounts:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM transactions_raw WHERE amount_cents < 0;")
print("Negative amounts:", cur.fetchone()[0])

# Quick check
cur.execute("SELECT COUNT(*) FROM transactions_raw;")
raw_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM transactions_validated;")
valid_count = cur.fetchone()[0]

print("raw_count =", raw_count)
print("valid_count =", valid_count)

conn.close()
