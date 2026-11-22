# Week 3 controlled incident: stopped API process

## Scope

Only my own foreground Uvicorn process on the learning EC2 instance was
stopped. No shared or production service was modified.

## Healthy baseline

The application loaded synthetic-claims-v1. Server logs recorded:
- GET /health: HTTP 200
- POST /predict with valid input: HTTP 200
- POST /predict missing claim_amount: HTTP 422

Evidence: evidence/week3-api-baseline.txt and evidence/week3-server.log.

## Simulation and observed failure

I stopped the foreground server using Ctrl+C.

At 2026-11-22T05:55:58+00:00:
- curl to 127.0.0.1:8000/health reported Connection refused.
- curl exit code was 7.
- The process check found no matching Uvicorn process.
- ss showed no TCP listener on port 8000.

Evidence: evidence/week3-incident-stopped.txt.

## Root cause

The manually launched application process had been intentionally stopped,
so no process was accepting connections on the expected local socket.
This was not an HTTP 422 validation failure: no HTTP response was received.

## Fix

Restarted from the project directory using the activated environment:

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

## Recovery verification

At 2026-11-22T05:56:38+00:00:
- Uvicorn was running as PID 6860.
- ss mapped the 127.0.0.1:8000 listener to Python PID 6860.
- The original health request returned HTTP 200.
- Body: {"status":"ok","model_loaded":true,"model_version":"synthetic-claims-v1"}

Evidence: evidence/week3-incident-recovered.txt.

The successful retest resolved the original symptom; a restart alone
would not have been sufficient evidence of recovery.

## Limitation

Manual foreground execution depends on the terminal session. A service
manager would be a separate improvement; systemd was not implemented.
