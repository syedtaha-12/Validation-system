import subprocess
import sys
import time

# Run every pipeline step in order and stop at the first failing step.
STEPS = [
    "create_db.py",
    "verify_db.py",
    "create_validated_view.py",
    "create_daily_summary.py",
    "create_account_summary.py",
    "export_reports.py",
    "verify_exports.py",
    "reconcile_totals.py",
    "reconcile_by_date.py",
    "reconcile_by_account.py",
]

start = time.perf_counter()
for step in STEPS:
    print(f"\n########## {step} ##########")
    step_start = time.perf_counter()
    result = subprocess.run([sys.executable, step])
    print(f"({step} took {time.perf_counter() - step_start:.2f}s)")
    if result.returncode != 0:
        print(f"\nPIPELINE FAILED at {step}")
        sys.exit(result.returncode)

print(f"\nPIPELINE PASSED: all {len(STEPS)} steps in {time.perf_counter() - start:.2f}s")
