# API test results

## Observed result

- Date: 16 October 2026
- Operating system: Windows
- Python: 3.14.5
- Pytest: 9.1.1
- Result: 12 passed, 1 warning
- Duration: 2.05 seconds

## Verified behavior

- Health endpoint returns success.
- Valid prediction returns the expected response structure.
- API prediction matches direct model inference.
- Invalid values, numeric strings, extra fields, and missing fields
  receive HTTP 422.
- Input key order does not change the prediction.
- Requests reuse the loaded model service and Pipeline objects.
- Responses include a non-negative latency header.

## Known dependency warning

The test run emitted a StarletteDeprecationWarning:

"Using httpx with starlette.testclient is deprecated;
install httpx2 instead."

This did not fail the tests. Dependency migration has not been
performed or validated in this milestone.

The complete test output is in pytest-output.txt.
