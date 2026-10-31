import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "data" / "claims_sample.csv"
OUTPUT_DIR = BASE_DIR / "output" 
OUTPUT_FILE = OUTPUT_DIR / "claims_summary.csv"


def classify_claim(claim_amount, threshold=50000):
    if claim_amount >= threshold:
        return "high"
    return "normal"

def validate_claim(claim_id, claim_amount, policy_tenure_days,
                   previous_claims, incident_delay_days):
    if not claim_id:
        raise ValueError("claim_id must not be empty")

    if claim_amount < 0:
        raise ValueError(f"{claim_id}: claim_amount must be at least 0")

    if policy_tenure_days < 1:
        raise ValueError(f"{claim_id}: policy_tenure_days must be at least 1")

    if previous_claims < 0:
        raise ValueError(f"{claim_id}: previous_claims must be at least 0")

    if incident_delay_days < 0:
        raise ValueError(f"{claim_id}: incident_delay_days must be at least 0")

if __name__ == "__main__":
    if not INPUT_FILE.exists():
        print(f"Input file not found: {INPUT_FILE}")
    else:
        summary_rows = []
        with INPUT_FILE.open(mode="r", newline="", encoding="utf-8") as input_file:
            reader = csv.DictReader(input_file)

            for row in reader:
                claim_id = row["claim_id"].strip()
                try:
                    claim_amount = int(row["claim_amount"])
                    policy_tenure_days = int(row["policy_tenure_days"])
                    previous_claims = int(row["previous_claims"])
                    incident_delay_days = int(row["incident_delay_days"])
                except ValueError as error:
                    raise ValueError(f"Invalid numeric value for claim {claim_id}: {error}")

                validate_claim(
                claim_id,
                    claim_amount,
                    policy_tenure_days,
                    previous_claims,
                    incident_delay_days
                )
                category = classify_claim(claim_amount)

                summary_rows.append(
                    {
                        "claim_id": claim_id,
                        "claim_amount": claim_amount,
                        "category": category,
                    }
                )
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        with OUTPUT_FILE.open(mode="w", newline="", encoding="utf-8") as output_file:
            fieldnames = ["claim_id", "claim_amount", "category"]
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(summary_rows)
        high_claims = sum(
            1 for row in summary_rows
            if row["category"] == "high"
        )

        normal_claims = len(summary_rows) - high_claims

        total_claim_amount = sum(
            row["claim_amount"]
            for row in summary_rows
        )

        print("Processed records:", len(summary_rows))
        print("High claims:", high_claims)
        print("Normal claims:", normal_claims)
        print("Total claim amount:", total_claim_amount)

