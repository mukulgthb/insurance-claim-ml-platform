## Debugging note
- Issue: A negative claim amount was introduced for `CLM-004`.
- Error: `ValueError: CLM-004: claim_amount must be at least 0`.
- Diagnosis: The validation function correctly rejected an amount below zero.
- Fix: Restored the valid amount of `10000` and reran the report.

- Issue: The input CSV file was missing.
- Error: `Input file not found: ...\week-2\data\claims_sample.csv`
- Diagnosis: The path existence check prevented file reading.
- Fix: Restored the input file to its expected name.

## Model inspection notes

- `fit()` learns values from training data. `StandardScaler` learns the mean and scale for each feature, while `LogisticRegression` learns coefficients and an intercept.
- `joblib.dump()` saves the fitted pipeline and related Python objects. `joblib.load()` restores them so the same trained pipeline can make predictions later.
- The original training dataset is not needed for inference because the fitted scaler statistics and classifier parameters are already stored in the model artifact.
- Feature names, order, and preprocessing must stay consistent because each learned coefficient is tied to one transformed feature position. Changing the order applies a coefficient to the wrong input.
- The training source code describes how to train a model; the saved model artifact contains the learned state produced after training.