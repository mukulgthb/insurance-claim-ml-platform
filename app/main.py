import logging
from contextlib import asynccontextmanager
from time import perf_counter

from fastapi import FastAPI, Request
from pydantic import BaseModel, ConfigDict, Field

from app.model import ModelService


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("claims-api")


class ClaimRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        strict=True,
    )

    claim_amount: float = Field(
        gt=0,
        le=1_000_000,
        allow_inf_nan=False,
        description="Synthetic claim amount in INR",
    )
    policy_tenure_days: int = Field(ge=1, le=36500)
    previous_claims: int = Field(ge=0, le=50)
    incident_delay_days: int = Field(ge=0, le=365)


class PredictionResponse(BaseModel):
    model_version: str
    requires_manual_review: bool
    review_probability: float = Field(ge=0, le=1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading model artifact")

    app.state.model_service = ModelService()

    logger.info(
        "Model loaded successfully: version=%s",
        app.state.model_service.version,
    )

    yield

    logger.info("Shutting down model service")
    del app.state.model_service


app = FastAPI(
    title="Synthetic Insurance Claims API",
    description="Educational model-serving service using synthetic data only.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def record_latency(request: Request, call_next):
    started = perf_counter()

    response = await call_next(request)

    duration_ms = (perf_counter() - started) * 1000

    response.headers["X-Process-Time-Ms"] = f"{duration_ms:.3f}"

    logger.info(
        "method=%s path=%s status=%s duration_ms=%.3f",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )

    return response


@app.get("/health")
def health(request: Request):
    service = request.app.state.model_service

    return {
        "status": "ok",
        "model_loaded": True,
        "model_version": service.version,
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: ClaimRequest, request: Request):
    service = request.app.state.model_service

    return service.predict(payload.model_dump())
