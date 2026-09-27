import sqlite3
import csv
from decimal import Decimal


def cents_to_amount(cents):
    """Format integer cents as a 2-decimal amount string, e.g. 55000 -> '550.00'."""
    return str(Decimal(cents or 0).scaleb(-2))


conn = sqlite3.connect("banking_qa.db")
cur = conn.cursor()

# Export daily_summary
cur.execute("SELECT date, transaction_count, total_amount_cents FROM daily_summary ORDER BY date;")
daily_rows = [(d, c, cents_to_amount(t)) for (d, c, t) in cur.fetchall()]

with open("daily_summary_report.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "transaction_count", "total_amount"])
    writer.writerows(daily_rows)

# Export account_summary
cur.execute("SELECT account_id, transaction_count, total_amount_cents FROM account_summary ORDER BY account_id;")
account_rows = [(a, c, cents_to_amount(t)) for (a, c, t) in cur.fetchall()]

with open("account_summary_report.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["account_id", "transaction_count", "total_amount"])
    writer.writerows(account_rows)

conn.close()

print("Reports exported:")
print(f"- daily_summary_report.csv ({len(daily_rows)} rows)")
print(f"- account_summary_report.csv ({len(account_rows)} rows)")
