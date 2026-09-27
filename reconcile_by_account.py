import sqlite3
import sys

conn = sqlite3.connect("banking_qa.db")
cur = conn.cursor()

# Source (validated layer)
cur.execute("""
SELECT
    account_id,
    COUNT(*) AS src_count,
    COALESCE(SUM(amount_cents), 0) AS src_total
FROM transactions_validated
GROUP BY account_id;
""")
src_rows = cur.fetchall()

# Report (account_summary)
cur.execute("""
SELECT
    account_id,
    transaction_count AS rpt_count,
    COALESCE(total_amount_cents, 0) AS rpt_total
FROM account_summary;
""")
rpt_rows = cur.fetchall()

conn.close()

src = {a: (c, t) for (a, c, t) in src_rows}
rpt = {a: (c, t) for (a, c, t) in rpt_rows}
all_accounts = sorted(set(src.keys()) | set(rpt.keys()))

# Only mismatches are printed, so the output stays readable at any volume.
print("=== Account-level Reconciliation ===")
failures = 0

for acc in all_accounts:
    src_count, src_total = src.get(acc, (0, 0))
    rpt_count, rpt_total = rpt.get(acc, (0, 0))

    if (src_count, src_total) != (rpt_count, rpt_total):
        failures += 1
        print(f"\nAccount: {acc}  FAIL")
        print(f"  Source -> count={src_count}, total_cents={src_total}")
        print(f"  Report -> count={rpt_count}, total_cents={rpt_total}")

print(f"Accounts checked: {len(all_accounts)} | mismatches: {failures}")

print("\n=== Overall Status ===")
print("REC-005 (By Account):", "PASS" if failures == 0 else "FAIL")

sys.exit(0 if failures == 0 else 1)
