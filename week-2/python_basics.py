claims = [
    {"claim_id": "CLM-001", "claim_amount": 25000, "previous_claims": 1},
    {"claim_id": "CLM-002", "claim_amount": 80000, "previous_claims": 2},
    {"claim_id": "CLM-003", "claim_amount": 50000, "previous_claims": 0},
]

def classify_claim(claim, threshold=50000):
    if claim["claim_amount"] >= threshold:
        return "high"
    else:
        return "normal"   


def total_claim_amount(claims):
    total = 0

    for claim in claims:
        total = total + claim["claim_amount"]

    return total        


if __name__ == "__main__":
    if claims:
        for claim in claims:
            category = classify_claim(claim)
            print(claim["claim_id"], claim["claim_amount"], category)
    else:
        print("No claims available.")

    print("Total claims:", len(claims))
    print("Total claim amount:", total_claim_amount(claims))

