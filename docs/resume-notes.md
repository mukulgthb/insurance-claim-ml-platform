# Resume checkpoint — 14 October 2026

## Confirmed working

- Windows Git Bash development environment.
- Python 3.14.5 virtual environment in .venv.
- Dependency installation and pip check.
- Synthetic training: 2,000 rows; 1,600 train / 400 test.
- Accuracy: 0.80.
- ROC AUC: 0.8258179857544198.
- Artifact generated: artifacts/model.joblib.
- ModelService loads the saved artifact.
- Direct inference works without retraining.
- Sample probability: 0.2249527593193222.
- Sample manual-review decision: false.
- Input key ordering check passed.
- Pipeline object reuse check passed.
- Artifact unchanged after inference.
- Missing-feature rejection check passed.

## Verify next

- Does app/main.py exist?
- Does the FastAPI application start?
- Does GET /health return 200?
- Does valid POST /predict return 200?
- Does invalid POST /predict return 422?
- Have request/response evidence files been captured?
- Does /docs open?


