import csv
import sqlite3
import sys
from decimal import Decimal


def read_csv_stats(path):
    """Return (row count, sum of total_amount in cents) for an exported report."""
    rows = 0
    total = Decimal(0)
    with open(path, "r", newline="") as f:
        for row in csv.DictReader(f):
            rows += 1
            total += Decimal(row["total_amount"])
    return rows, int(total * 100)


conn = sqlite3.connect("banking_qa.db")
cur = conn.cursor()

cur.execute("SELECT COUNT(*), COALESCE(SUM(total_amount_cents), 0) FROM daily_summary;")
db_daily = cur.fetchone()
cur.execute("SELECT COUNT(*), COALESCE(SUM(total_amount_cents), 0) FROM account_summary;")
db_acc = cur.fetchone()

conn.close()

csv_daily = read_csv_stats("daily_summary_report.csv")
csv_acc = read_csv_stats("account_summary_report.csv")

print("DB daily_summary   (rows, cents):", db_daily, "| CSV:", csv_daily)
print("DB account_summary (rows, cents):", db_acc, "| CSV:", csv_acc)

daily_ok = tuple(db_daily) == csv_daily
acc_ok = tuple(db_acc) == csv_acc

print("\nStatus:")
print("Daily export:  ", "PASS" if daily_ok else "FAIL")
print("Account export:", "PASS" if acc_ok else "FAIL")

sys.exit(0 if daily_ok and acc_ok else 1)
