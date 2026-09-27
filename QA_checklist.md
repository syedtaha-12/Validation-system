# QA Checklist

Dataset: `transactions.csv` from `generate_transactions.py` (seed 42): 5,050 raw rows, 250 accounts, 92 days.
Run with `python run_pipeline.py`. Last run: 2026-09-26, all 10 steps PASS in under 1 second.

## Data Generation
- [x] Synthetic dataset generated with a fixed seed (same seed = same file)
- [x] Known data quality issues included on purpose: missing amounts, negative amounts, duplicate rows

## Ingestion
- [x] Raw data bulk-loaded into `transactions_raw` (5,050 rows)
- [x] Amounts stored as integer cents; missing amounts stored as `NULL`, not `0`
- [x] Re-running `create_db.py` rebuilds the table (no duplicated loads)
- [x] Row count verified after ingestion (`verify_db.py`)

## Validation Layer
- [x] `transactions_validated` view created
- [x] Duplicate `transaction_id`s detected (50) and deduplicated (one row per ID)
- [x] `NULL` amounts filtered out (102 raw rows)
- [x] Negative amounts filtered out (103 raw rows)
- [x] Raw vs. validated counts reported: 5,050 → 4,799

## Reporting
- [x] `daily_summary` generated from validated data (92 dates)
- [x] `account_summary` generated from validated data (250 accounts)

## Export
- [x] Reports exported: `daily_summary_report.csv`, `account_summary_report.csv`
- [x] Exported row counts match the database tables
- [x] Exported amount totals match the database tables (exact, in cents)

## Reconciliation
- [x] REC-001 PASS: total amount, validated vs. `daily_summary`
- [x] REC-002 PASS: transaction count, validated vs. `daily_summary`
- [x] REC-003 PASS: count and total per date (92 dates, 0 mismatches)
- [x] REC-004 PASS: count and total per account (250 accounts, 0 mismatches)

## Automation
- [x] Every check script exits with code `1` on FAIL
- [x] `run_pipeline.py` stops at the first failing step
- [x] Pipeline can be re-run without deleting `banking_qa.db`
- [x] Negative test: a 1-cent change to one account's total makes REC-004 FAIL (exit code 1)

## Open Items
- [ ] Confirm with the business team whether negative amounts (withdrawals, refunds) should be treated as invalid
