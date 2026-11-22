# Week 3 API contract

## Existing routes

GET /health returns status, model_loaded and model_version.

POST /predict accepts an application/json body with four required fields:

| Field | Type | Constraints |
|---|---|---|
| claim_amount | float | > 0, <= 1000000; finite |
| policy_tenure_days | int | 1 to 36500 |
| previous_claims | int | 0 to 50 |
| incident_delay_days | int | 0 to 365 |

ClaimRequest uses strict validation and forbids extra fields.
Numeric strings should not be used in place of numbers.

Sample request:

{"claim_amount":25000,"policy_tenure_days":400,"previous_claims":1,"incident_delay_days":3}

Successful responses contain:
- model_version: string
- requires_manual_review: boolean
- review_probability: number from 0 to 1

The valid request produced HTTP 200; see evidence/week3-api-baseline.txt
for the actual response values.

Omitting claim_amount produced HTTP 422. The validation response identifies
type "missing", location ["body","claim_amount"], and "Field required".
See baseline evidence for the exact response body.

## Execution flow

Application startup constructs ModelService and loads the trusted Joblib
artifact into app.state.

JSON -> Pydantic ClaimRequest validation -> payload.model_dump() ->
ModelService.predict -> ordered pandas DataFrame -> fitted pipeline
(scaler and classifier) -> positive-class probability -> threshold
comparison -> response-model handling -> JSON.

The feature order is:
1. claim_amount
2. policy_tenure_days
3. previous_claims
4. incident_delay_days

ModelService verifies metadata feature order and fitted feature names at
startup. Each prediction also rejects missing or extra feature keys.

It selects the positive-class probability using pipeline.classes_ and
metadata. The review decision is probability >= metadata threshold.

## Proposed claim_id enhancement: design only, not implemented

Add an optional claim_id string to request and response, defaulting to
None so existing clients can omit it. Proposed validation: 1-64 ASCII
letters, digits, hyphens or underscores when provided.

In the route:
1. Extract claim_id separately.
2. Call payload.model_dump(exclude={"claim_id"}).
3. Send only the original four model features to ModelService.predict.
4. Add the unchanged claim_id to the returned response.

Do not simply add claim_id to ClaimRequest while keeping model_dump()
unchanged: ModelService currently rejects any extra feature key.

claim_id identifies the business claim, not a trained numerical feature.
Changing classifier inputs would violate the fitted feature contract.

For independent claims A and B, responses should echo their own IDs.
A client should associate responses by ID rather than arrival order:
if B finishes first, it must still update claim B, not claim A.
The caller must use IDs that are unique within the correlation scope.

Proposed tests, not executed:
- Existing requests without claim_id still succeed.
- A supplied claim_id is echoed exactly.
- Adding an ID does not change probability or model feature selection.
- Invalid IDs are rejected.
- Simulated responses handled in B/A order remain mapped to B/A by ID.

No application or test code was changed for this proposal.
