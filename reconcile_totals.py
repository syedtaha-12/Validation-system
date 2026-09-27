import sqlite3
import sys

conn = sqlite3.connect("banking_qa.db")
cur = conn.cursor()

# --- REC-001: Total Amount reconciliation (integer cents, exact) ---
cur.execute("SELECT COALESCE(SUM(amount_cents), 0) FROM transactions_validated;")
validated_total = cur.fetchone()[0]

cur.execute("SELECT COALESCE(SUM(total_amount_cents), 0) FROM daily_summary;")
summary_total = cur.fetchone()[0]

# --- REC-002: Transaction count reconciliation ---
cur.execute("SELECT COUNT(*) FROM transactions_validated;")
validated_count = cur.fetchone()[0]

cur.execute("SELECT COALESCE(SUM(transaction_count), 0) FROM daily_summary;")
summary_count = cur.fetchone()[0]

conn.close()

print("=== Reconciliation Results ===")
print(f"Validated total amount (cents): {validated_total}")
print(f"Summary total amount (cents):   {summary_total}")
print(f"Validated txn count:            {validated_count}")
print(f"Summary txn count:              {summary_count}")

# PASS/FAIL checks
total_pass = (validated_total == summary_total)
count_pass = (validated_count == summary_count)

print("\n=== Status ===")
print("REC-001 (Total Amount):", "PASS" if total_pass else "FAIL")
print("REC-002 (Txn Count):   ", "PASS" if count_pass else "FAIL")

sys.exit(0 if total_pass and count_pass else 1)
