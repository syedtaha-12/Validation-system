import argparse
import csv
import random
from datetime import date, timedelta

# Generate a synthetic transactions.csv with realistic data quality issues:
# missing amounts, negative amounts, and duplicated transaction rows.

parser = argparse.ArgumentParser(description="Generate synthetic banking transactions.")
parser.add_argument("--rows", type=int, default=5000, help="number of unique transactions")
parser.add_argument("--accounts", type=int, default=250, help="number of distinct accounts")
parser.add_argument("--days", type=int, default=92, help="number of days covered, from 2024-10-01")
parser.add_argument("--seed", type=int, default=42, help="random seed (same seed = same file)")
parser.add_argument("--out", default="transactions.csv", help="output CSV path")
args = parser.parse_args()

rng = random.Random(args.seed)
start = date(2024, 10, 1)

MISSING_RATE = 0.02
NEGATIVE_RATE = 0.02
DUPLICATE_RATE = 0.01

rows = []
missing = negative = 0
for i in range(args.rows):
    cents = rng.randint(100, 500_000)  # 1.00 to 5,000.00
    r = rng.random()
    if r < MISSING_RATE:
        amount = ""
        missing += 1
    elif r < MISSING_RATE + NEGATIVE_RATE:
        amount = f"-{cents // 100}.{cents % 100:02d}"
        negative += 1
    else:
        amount = f"{cents // 100}.{cents % 100:02d}"

    rows.append([
        100001 + i,
        f"A{rng.randint(1, args.accounts):04d}",
        amount,
        (start + timedelta(days=rng.randrange(args.days))).isoformat(),
    ])

# Insert exact copies of some rows at random positions.
duplicates = int(args.rows * DUPLICATE_RATE)
copies = [list(rows[i]) for i in rng.sample(range(len(rows)), duplicates)]
for copy in copies:
    rows.insert(rng.randint(0, len(rows)), copy)

with open(args.out, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["transaction_id", "account_id", "amount", "date"])
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to {args.out}")
print(f"  unique transactions: {args.rows}")
print(f"  missing amounts:     {missing}")
print(f"  negative amounts:    {negative}")
print(f"  duplicate rows:      {duplicates}")
print(f"  expected valid rows: {args.rows - missing - negative}")
