import sqlite3
import sys

conn = sqlite3.connect("banking_qa.db")
cur = conn.cursor()

# Source aggregates (validated layer)
cur.execute("""
SELECT
  date,
  COUNT(*) AS src_count,
  COALESCE(SUM(amount_cents), 0) AS src_total
FROM transactions_validated
GROUP BY date;
""")
src_rows = cur.fetchall()

# Report aggregates (daily_summary)
cur.execute("""
SELECT
  date,
  transaction_count AS rpt_count,
  COALESCE(total_amount_cents, 0) AS rpt_total
FROM daily_summary;
""")
rpt_rows = cur.fetchall()

conn.close()

# Convert results into dicts keyed by date
src = {d: (c, t) for (d, c, t) in src_rows}
rpt = {d: (c, t) for (d, c, t) in rpt_rows}

all_dates = sorted(set(src.keys()) | set(rpt.keys()))

# Only mismatches are printed, so the output stays readable at any volume.
print("=== Date-level Reconciliation ===")
failures = 0

for d in all_dates:
    src_count, src_total = src.get(d, (0, 0))
    rpt_count, rpt_total = rpt.get(d, (0, 0))

    if (src_count, src_total) != (rpt_count, rpt_total):
        failures += 1
        print(f"\nDate: {d}  FAIL")
        print(f"  Source (validated) -> count={src_count}, total_cents={src_total}")
        print(f"  Report (summary)   -> count={rpt_count}, total_cents={rpt_total}")

print(f"Dates checked: {len(all_dates)} | mismatches: {failures}")

print("\n=== Overall Status ===")
print("REC-004 (By Date):", "PASS" if failures == 0 else "FAIL")

sys.exit(0 if failures == 0 else 1)
