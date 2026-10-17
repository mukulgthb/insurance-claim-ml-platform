from pathlib import Path

import joblib
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "artifacts" / "model.joblib"

EXPECTED_FEATURES = [
    "claim_amount",
    "policy_tenure_days",
    "previous_claims",
    "incident_delay_days",
]


class ModelService:
    def __init__(self, artifact_path=MODEL_PATH):
        artifact_path = Path(artifact_path)

        if not artifact_path.is_file():
            raise FileNotFoundError(
                f"Model artifact not found: {artifact_path}. "
                "Run: python -m training.train"
            )

        artifact = joblib.load(artifact_path)

        self.pipeline = artifact["pipeline"]
        self.metadata = artifact["metadata"]

        if self.metadata["features"] != EXPECTED_FEATURES:
            raise ValueError(
                "Artifact metadata does not match the expected feature order."
            )

        if list(self.pipeline.feature_names_in_) != EXPECTED_FEATURES:
            raise ValueError(
                "Fitted pipeline does not match the expected feature names."
            )

        self.version = self.metadata["model_version"]
        self.threshold = float(self.metadata["threshold"])
        self.positive_class = self.metadata["positive_class"]

        classes = list(self.pipeline.classes_)
        self.positive_index = classes.index(self.positive_class)

    def predict(self, values):
        received = set(values)
        expected = set(EXPECTED_FEATURES)

        if received != expected:
            missing = sorted(expected - received)
            extra = sorted(received - expected)

            raise ValueError(
                f"Feature mismatch. Missing: {missing}; extra: {extra}"
            )

        frame = pd.DataFrame(
            [[values[name] for name in EXPECTED_FEATURES]],
            columns=EXPECTED_FEATURES,
        )

        probability = float(
            self.pipeline.predict_proba(frame)[0, self.positive_index]
        )

        return {
            "model_version": self.version,
            "requires_manual_review": probability >= self.threshold,
            "review_probability": probability,
        }
