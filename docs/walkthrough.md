# Two-Minute Project Walkthrough

## Requirement

The requirement was to demonstrate a complete local model lifecycle
using only synthetic or public data: train a classifier, save its
artifact, and expose validated predictions through a REST API.

## Design

I built a synthetic insurance-claims manual-review example.

Training is separate from serving. The training script creates the
artifact, and the API loads that trusted artifact during startup.
Requests reuse the loaded model rather than retraining it.

## Implementation

The training script generates 2,000 synthetic examples and splits them
into 1,600 training rows and 400 test rows.

A scikit-learn Pipeline combines StandardScaler and logistic regression.
The saved joblib artifact contains the fitted Pipeline and metadata,
including feature names, a threshold, and a model-version label.

FastAPI exposes GET /health and POST /predict. Pydantic validates
incoming JSON, and the serving code constructs features in the expected
order before invoking the Pipeline.

The response contains a review decision, probability, and model version.
Middleware records request status and server-side processing duration.

## Validation

The recorded synthetic accuracy was 0.80 and ROC AUC approximately 0.826.
These results do not establish real insurance suitability.

Direct inference and API predictions agree. All 12 automated tests
passed, covering health, validation, feature ordering, model reuse,
prediction consistency, and latency headers.

## Limitations

This is a localhost-only educational service without authentication,
immutable artifact versioning, cloud deployment, or production monitoring.
One dependency deprecation warning was recorded during testing.

I built the implementation with guidance. My next goal is to explain
and modify each component independently.
