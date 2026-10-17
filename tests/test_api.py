import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.model import ModelService


VALID_REQUEST = {
    "claim_amount": 25000,
    "policy_tenure_days": 400,
    "previous_claims": 1,
    "incident_delay_days": 3,
}


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "ok"
    assert body["model_loaded"] is True
    assert body["model_version"] == "synthetic-claims-v1"


def test_valid_prediction(client):
    response = client.post("/predict", json=VALID_REQUEST)

    assert response.status_code == 200

    body = response.json()

    assert body["model_version"] == "synthetic-claims-v1"
    assert isinstance(body["requires_manual_review"], bool)
    assert 0 <= body["review_probability"] <= 1


def test_api_matches_direct_inference(client):
    expected = ModelService().predict(VALID_REQUEST)

    response = client.post("/predict", json=VALID_REQUEST)

    assert response.status_code == 200

    actual = response.json()

    assert actual["model_version"] == expected["model_version"]
    assert (
        actual["requires_manual_review"]
        == expected["requires_manual_review"]
    )
    assert actual["review_probability"] == pytest.approx(
        expected["review_probability"]
    )


@pytest.mark.parametrize(
    "changes",
    [
        {"claim_amount": -500},
        {"policy_tenure_days": 0},
        {"previous_claims": "1"},
        {"incident_delay_days": -1},
        {"unexpected_field": 123},
    ],
    ids=[
        "negative-amount",
        "zero-tenure",
        "numeric-string",
        "negative-delay",
        "extra-field",
    ],
)
def test_invalid_input(client, changes):
    payload = {**VALID_REQUEST, **changes}

    response = client.post("/predict", json=payload)

    assert response.status_code == 422
    assert "detail" in response.json()


def test_missing_field(client):
    payload = dict(VALID_REQUEST)
    del payload["claim_amount"]

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_input_key_order_does_not_change_prediction(client):
    reordered = dict(reversed(list(VALID_REQUEST.items())))

    first = client.post("/predict", json=VALID_REQUEST)
    second = client.post("/predict", json=reordered)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()


def test_loaded_model_is_reused(client):
    original_service = app.state.model_service
    original_pipeline = original_service.pipeline

    for _ in range(3):
        response = client.post("/predict", json=VALID_REQUEST)
        assert response.status_code == 200

    assert app.state.model_service is original_service
    assert app.state.model_service.pipeline is original_pipeline


def test_latency_header(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert "X-Process-Time-Ms" in response.headers
    assert float(response.headers["X-Process-Time-Ms"]) >= 0
