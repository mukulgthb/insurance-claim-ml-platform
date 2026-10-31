import pandas as pd
from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent
MODEL_FILE = REPO_ROOT / "artifacts" / "model.joblib"

if __name__ == "__main__":
    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            f"Model artifact not found: {MODEL_FILE}. "
            "Run: python -m training.train"
        )

    artifact = joblib.load(MODEL_FILE)
    print("Top-level artifact keys:", artifact.keys())
    pipeline = artifact["pipeline"]
    metadata = artifact["metadata"]
    print("Pipeline:", pipeline)
    print("Pipeline stages:", pipeline.named_steps.keys())
    print("Metadata keys:", metadata.keys())

    scaler = pipeline.named_steps["scaler"]
    classifier = pipeline.named_steps["classifier"]
    print("Scaler mean:", scaler.mean_)
    print("Scaler scale:", scaler.scale_)
    print("Classifier coefficients:", classifier.coef_)
    print("Classifier intercept:", classifier.intercept_)
    print("Classifier classes:", classifier.classes_)

    print("Features:", metadata["features"])
    print("Model version:", metadata["model_version"])
    print("Threshold:", metadata["threshold"])

    frame = pd.DataFrame(
        [[25000, 400, 1, 3]],
        columns=metadata["features"],
    )

    probabilities = pipeline.predict_proba(frame)
    positive_probability = probabilities[0, 1]

    print("Input frame:")
    print(frame)
    print("Probability shape:", probabilities.shape)
    print("Positive-class probability:", positive_probability)
    print("Threshold:", metadata["threshold"])

    predicted_class = int(positive_probability >= metadata["threshold"])
    print("Predicted class:", predicted_class)
    print(
        "Decision:",
        "positive" if predicted_class == 1 else "negative",
    )