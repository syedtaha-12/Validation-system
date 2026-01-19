# Automated Reporting Quality Assurance & Validation System

## What this is
A self-initiated Quality Engineering project that simulates a banking-style reporting pipeline and validates reporting accuracy end-to-end.

## Architecture
transactions.csv → transactions_raw (SQLite) → transactions_validated → {daily_summary, account_summary} → CSV reports → Power BI dashboard

## Pipeline
1) Ingest raw transactions (CSV → SQLite staging table)
2) Create validated layer (filters invalid records)
3) Generate reporting tables:
   - daily_summary (by date)
   - account_summary (by account)
4) Export reports to CSV
5) Reconcile reporting outputs against validated source data (overall + partition-level)

## QA checks implemented
- Completeness: row counts after ingestion
- Validity: null / negative amount detection
- Integrity: duplicate transaction checks
- Reporting accuracy: reconciliation of sums and counts
  - overall totals
  - by date
  - by account

## Validation Results
- Reconciliation PASS (Totals)
- Reconciliation PASS (By Date)
- Reconciliation PASS (By Account)

## Key Features
- Raw transaction ingestion into a staging table
- Data quality validation (nulls, negatives, duplicates)
- Creation of reporting tables:
  - Daily summary (by date)
  - Account summary (by account)
- Automated reconciliation checks:
  - Overall totals
  - Date-level
  - Account-level
- Report export for BI consumption
- Dashboard validation (Power BI)

## QA Techniques Applied
- Data completeness checks
- Business rule validation
- Aggregation validation
- Reconciliation across pipeline layers
- Automation and repeatability

## Tech Stack
- Python
- SQL
- SQLite
- Power BI
- CSV-based reporting

## What I Learned
Designing QA checks for reporting pipelines, implementing reconciliation to ensure correctness across layers, and validating BI outputs against trusted aggregates.

## How to Run
```bash
python create_db.py
python create_validated_view.py
python create_daily_summary.py
python create_account_summary.py
python export_reports.py
python reconcile_totals.py
python reconcile_by_date.py
python reconcile_by_account.py

