# Automated Reporting Quality Assurance & Validation System

## Overview

A self-initiated **Quality Engineering** project that simulates a **banking-style reporting pipeline** and validates reporting accuracy **end-to-end** using SQL, Python automation, and reconciliation checks.

---

## Architecture

```
transactions.csv
  → transactions_raw        (SQLite staging table)
  → transactions_validated  (SQL view: filters invalid amounts)
  → daily_summary / account_summary  (reporting tables)
  → CSV reports             (ready for Power BI or other BI tools)
```

---

## Pipeline

1. **Ingest** raw transactions (CSV → SQLite staging table `transactions_raw`). Missing amounts are stored as `NULL`, not `0`, so they can be detected later.
2. **Validate:** create the `transactions_validated` view, which removes rows with `NULL` or negative amounts.
3. **Report:** build two summary tables from the validated data:
   - `daily_summary`: transaction count and total amount by date
   - `account_summary`: transaction count and total amount by account
4. **Export** both reports to CSV for downstream use.
5. **Reconcile:** check that the report totals match the validated source data.

---

## QA Checks Implemented

### Data Quality
- **Completeness:** row counts after ingestion (`verify_db.py`) and raw vs. validated counts (`create_validated_view.py`)
- **Validity:** `NULL` and negative amounts are filtered out of the validated layer
- **Integrity:** duplicate `transaction_id`s are detected and removed

### Reporting Accuracy (Reconciliation)
| ID | Check | Script |
|----|-------|--------|
| REC-002 | Total amount: validated source vs. `daily_summary` | `reconcile_totals.py` |
| REC-003 | Transaction count: validated source vs. `daily_summary` | `reconcile_totals.py` |
| REC-004 | Count and total per date | `reconcile_by_date.py` |
| REC-005 | Count and total per account | `reconcile_by_account.py` |

### Export Accuracy
- Row counts in each exported CSV match the database tables (`verify_exports.py`)

---

## Validation Results

On the sample dataset (6 raw rows → 3 validated rows):

- ✅ REC-002 / REC-003: Overall totals and counts: PASS
- ✅ REC-004: By date: PASS
- ✅ REC-005: By account: PASS
- ✅ Export row counts: PASS

---

## Known Limitations & Next Steps

- ~~Duplicates are not removed~~ **Fixed:** the validated view now keeps one row per `transaction_id`, and a check prints any duplicate IDs found in the raw data.
- **Re-running `create_db.py` loads the data again**, which duplicates every row in the raw table. The validated view still keeps one row per `transaction_id`, and the duplicate check reports the repeated IDs.
- **Negative amounts are treated as invalid.** This is a business rule chosen for this dataset. In a real bank, negatives could be valid withdrawals or refunds, so this rule would be confirmed with the business team.
- **Floating-point amounts** are compared with `==`. For real financial data, amounts should be stored as integer cents or decimals.

---

## Tech Stack

- **Python** (`sqlite3`, `csv`)
- **SQL**
- **SQLite**
- **CSV-based reporting**

---

## What I Learned

How to design QA checks for a reporting pipeline, how to use reconciliation to prove reports are correct across several dimensions, and why reconciliation alone is not enough. Checks on the source data (like duplicate detection) are also needed.

---

## How to Run

```bash
python create_db.py
python verify_db.py
python create_validated_view.py
python create_daily_summary.py
python create_account_summary.py
python export_reports.py
python verify_exports.py
python reconcile_totals.py
python reconcile_by_date.py
python reconcile_by_account.py
```

To start fresh, delete `banking_qa.db` before running `create_db.py`.
