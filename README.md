# Automated Reporting Quality Assurance & Validation System

## Overview
A self-initiated **Quality Engineering** project that simulates a **banking-style reporting pipeline** and validates reporting accuracy **end-to-end** using SQL, Python automation, and reconciliation checks.

---

## Architecture

transactions.csv  
→ transactions_raw (SQLite)  
→ transactions_validated  
→ daily_summary / account_summary  
→ CSV reports  
→ Power BI dashboard

---

## Pipeline
1. Ingest raw transactions (CSV → SQLite staging table)
2. Create a validated data layer (filters invalid records)
3. Generate reporting tables:
   - **daily_summary** (by date)
   - **account_summary** (by account)
4. Export reports to CSV for downstream consumption
5. Reconcile reporting outputs against validated source data

---

## QA Checks Implemented

### Data Quality
- **Completeness:** Row-count validation after ingestion
- **Validity:** Detection of null and negative transaction amounts
- **Integrity:** Duplicate transaction identification

### Reporting Accuracy (Reconciliation)
- Overall totals (sums and counts)
- Date-level reconciliation
- Account-level reconciliation

---

## Validation Results
- ✅ Reconciliation PASS — Overall Totals  
- ✅ Reconciliation PASS — By Date  
- ✅ Reconciliation PASS — By Account  

---

## Key Features
- Raw transaction ingestion into a staging table
- Data quality validation prior to reporting
- Multi-dimensional reporting (time-based and account-based)
- Automated reconciliation with PASS/FAIL outcomes
- Report export for BI tools
- Dashboard validation using Power BI

---

## QA Techniques Applied
- Data completeness checks
- Business rule validation
- Aggregation and grouping validation
- Reconciliation across pipeline layers
- Automation and repeatability

---

## Tech Stack
- **Python**
- **SQL**
- **SQLite**
- **Power BI**
- **CSV-based reporting**

---

## What I Learned
Designing QA checks for reporting pipelines, implementing reconciliation to ensure correctness across multiple dimensions, and validating BI outputs against trusted aggregates.

---

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



