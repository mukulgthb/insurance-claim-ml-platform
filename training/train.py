import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT / "artifacts"

FEATURES = [
    "claim_amount",
    "policy_tenure_days",
    "previous_claims",
    "incident_delay_days",
]

MODEL_VERSION = "synthetic-claims-v1"


def generate_data(rows=2000, seed=42):
    rng = np.random.default_rng(seed)

    features = pd.DataFrame(
        {
            "claim_amount": rng.uniform(1000, 100000, rows),
            "policy_tenure_days": rng.integers(1, 3651, rows),
            "previous_claims": rng.integers(0, 6, rows),
            "incident_delay_days": rng.integers(0, 61, rows),
        }
    )

    # Invented relationship for learning; not real insurance guidance.
    score = (
        -1.0
        + (features["claim_amount"] - 40000) / 25000
        - features["policy_tenure_days"] / 2500
        + 0.45 * features["previous_claims"]
        + 0.04 * features["incident_delay_days"]
    )

    probability = 1 / (1 + np.exp(-score))
    labels = rng.binomial(1, probability)

    return features[FEATURES], labels


def main():
    print("STEP 1: Generate synthetic data")
    features, labels = generate_data()

    print(f"Rows: {len(features)}")
    print(f"Features: {list(features.columns)}")

    preview = features.head().copy()
    preview["requires_manual_review"] = labels[:5]

    print("\nFirst five synthetic examples:")
    print(preview.to_string(index=False))

    print("\nSTEP 2: Split training and test data")
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        labels,
        test_size=0.2,
        random_state=42,
        stratify=labels,
    )

    print(f"Training rows: {len(x_train)}")
    print(f"Test rows: {len(x_test)}")

    print("\nSTEP 3: Fit scaler and classifier")
    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    random_state=42,
                ),
            ),
        ]
    )

    pipeline.fit(x_train, y_train)

    print("\nSTEP 4: Evaluate on held-out test data")
    predictions = pipeline.predict(x_test)

    positive_index = list(pipeline.classes_).index(1)
    probabilities = pipeline.predict_proba(x_test)[:, positive_index]

    metrics = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "roc_auc": float(roc_auc_score(y_test, probabilities)),
        "train_rows": len(x_train),
        "test_rows": len(x_test),
    }

    print(json.dumps(metrics, indent=2))

    metadata = {
        "model_version": MODEL_VERSION,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "features": FEATURES,
        "target": "requires_manual_review",
        "positive_class": 1,
        "threshold": 0.5,
        "data_source": "locally generated synthetic data",
        "random_seed": 42,
        "python_version": platform.python_version(),
        "sklearn_version": sklearn.__version__,
        "metrics": metrics,
    }

    artifact = {
        "pipeline": pipeline,
        "metadata": metadata,
    }

    print("\nSTEP 5: Save model artifact and metadata")
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    model_path = ARTIFACT_DIR / "model.joblib"
    metadata_path = ARTIFACT_DIR / "metadata.json"

    joblib.dump(artifact, model_path)

    metadata_path.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    print(f"Model saved: {model_path}")
    print(f"Metadata saved: {metadata_path}")
    print(f"Model size: {model_path.stat().st_size} bytes")
    print("\nTraining completed successfully.")


if __name__ == "__main__":
    main()
