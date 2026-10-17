# Why local FastAPI for Phase 0?

A local FastAPI service is appropriate for this milestone because the goal is to understand and demonstrate the model-serving lifecycle before introducing cloud infrastructure. It keeps training, artifact loading, request validation, and prediction visible in a small application that I can run and debug directly.

The training script generates synthetic claims, separates training and test data, fits a preprocessing and classification Pipeline, and saves the fitted artifact. The application loads that artifact during startup. Each prediction request uses the existing in-memory Pipeline rather than retraining or reading the artifact again. Pydantic enforces the input contract, and responses include the model version, review probability, and routing decision.

This approach also supports practical validation. I tested health checks, valid and invalid predictions, agreement with direct inference, feature ordering, model reuse, and latency headers. Request logs record operational information without recording claim bodies. These checks provide evidence that the implementation behaves as intended, although synthetic evaluation does not establish real insurance usefulness.

The local service is deliberately limited. It has no authentication, production availability guarantee, immutable model registry, or automated deployment. It should remain bound to localhost.

A managed serving platform becomes preferable when the workload needs authenticated remote access, managed compute, repeatable deployment, monitoring, and scaling. Azure Machine Learning managed online endpoints provide relevant capabilities, including authentication options and integration with Azure Monitor for metrics and autoscaling. The decision should depend on traffic, latency, governance, operational ownership, portability, and cost. For Phase 0, those additional platform concerns would distract from proving the core lifecycle.
