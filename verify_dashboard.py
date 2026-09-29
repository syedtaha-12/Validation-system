import sqlite3

# Prints the numbers the Power BI dashboard SHOULD show,
# calculated straight from the clean data (transactions_validated).
# Compare each line with the matching visual on the dashboard.

conn = sqlite3.connect("banking_qa.db")
cur = conn.cursor()


def dollars(cents):
    """Turn integer cents into a $ string, e.g. 1193757078 -> $11,937,570.78"""
    return f"${cents // 100:,}.{cents % 100:02d}"


# 1. The 4 cards
cur.execute("""
SELECT COUNT(*), SUM(amount_cents), COUNT(DISTINCT account_id)
FROM transactions_validated;
""")
count, total, accounts = cur.fetchone()

print("=== Cards ===")
print("Total Amount:   ", dollars(total))
print("Transactions:   ", f"{count:,}")
print("Avg Transaction:", f"${total / count / 100:,.2f}")
print("Accounts:       ", accounts)

# 2. Line chart: busiest and quietest day
cur.execute("""
SELECT date, SUM(amount_cents) AS day_total
FROM transactions_validated
GROUP BY date
ORDER BY day_total DESC;
""")
days = cur.fetchall()

print("\n=== Line chart ===")
print("Days plotted:   ", len(days))
print("Highest day:    ", days[0][0], dollars(days[0][1]))
print("Lowest day:     ", days[-1][0], dollars(days[-1][1]))

# 3. Bar chart: top 10 accounts
cur.execute("""
SELECT account_id, SUM(amount_cents) AS acc_total
FROM transactions_validated
GROUP BY account_id
ORDER BY acc_total DESC
LIMIT 10;
""")

print("\n=== Top 10 accounts ===")
for rank, (acc, acc_total) in enumerate(cur.fetchall(), start=1):
    print(f"{rank:>2}. {acc}  {dollars(acc_total)}")

conn.close()