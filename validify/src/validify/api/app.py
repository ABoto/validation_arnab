"""
api/app.py — FastAPI application with three routes.

─────────────────────────────────────────────────────────
DAY 4 TASK
─────────────────────────────────────────────────────────
Implement a minimal FastAPI application with these three routes:

  GET  /health
    Returns: {"status": "ok", "version": "0.1.0"}

  POST /validate
    Accepts:  UploadFile (a CSV file)
    Process:
      1. Read the uploaded file bytes and decode to a string.
      2. Parse as CSV using csv.DictReader(io.StringIO(content)).
      3. Load rules from config/rules.yaml.
      4. Run validation using your engine from runner.py.
      5. Build a Report from the results.
      6. Store the Report in the module-level REPORTS dict keyed by a run_id.
      7. Return: {"run_id": "<uuid>", "summary": {"total": N, "passed": N, ...}}

  GET  /reports/{run_id}
    Returns the stored Report as JSON.
    Returns HTTP 404 if run_id is not found.

─────────────────────────────────────────────────────────
TIPS
─────────────────────────────────────────────────────────
  - Use uuid.uuid4() to generate run IDs.
  - Store reports in a module-level dict (not a database).
  - Run with: uvicorn validify.api.app:app --reload
  - The config file is at config/rules.yaml relative to the project root.
    Pass its path as an argument or use an environment variable.
"""

import csv
import io
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile  # noqa: F401

# Add your own imports from validify modules as needed.

# In-memory report store: {run_id: Report}
REPORTS: dict = {}


def create_app() -> FastAPI:
    app = FastAPI(
        title="Validify",
        version="0.1.0",
        description="Enterprise Data Validation & Processing Service",
    )

    # ---------------------------------------------------------------------------
    # YOUR ROUTES BELOW
    # ---------------------------------------------------------------------------

    from validify.rules.built_in import RuleFactory
    from validify.engine.runner import run_threaded
    from validify.core.models import Report

    # -------------------------
    # Health Check
    # -------------------------
    @app.get("/health")
    def health():
        return {"status": "ok", "version": "0.1.0"}

    # -------------------------
    # Validate CSV File
    # -------------------------
    @app.post("/validate")
    async def validate(file: UploadFile):
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are accepted")

        # Read uploaded file content (bytes → text → DictReader)
        content = await file.read()
        text = content.decode()
        rows = list(csv.DictReader(io.StringIO(text)))

        # Load rules dynamically from YAML
        rules = RuleFactory.from_config("config/rules.yaml")

        # Run threaded validation
        results = run_threaded(rows, rules)

        # Build report
        total = len(results)
        passed = sum(r.passed for r in results)
        failed = total - passed

        report = Report(total, passed, failed, results)

        # Create unique run_id
        run_id = str(uuid.uuid4())
        REPORTS[run_id] = report

        return {
            "run_id": run_id,
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "pass_rate": report.pass_rate,
            },
        }

    # -------------------------
    # Retrieve Report by ID
    # -------------------------
    @app.get("/reports/{run_id}")
    def get_report(run_id: str):
        if run_id not in REPORTS:
            raise HTTPException(status_code=404, detail="Report not found")

        report: Report = REPORTS[run_id]

        return {
            "total": report.total,
            "passed": report.passed,
            "failed": report.failed,
            "pass_rate": report.pass_rate,
            "results": [
                {
                    "field": r.field,
                    "rule": r.rule,
                    "passed": r.passed,
                    "message": r.message,
                }
                for r in report.results
            ],
        }

    return app


app = create_app()




