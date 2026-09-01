import os
import sys
import pandas as pd


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(BASE_DIR)


from src.decision_engine import FraudDecisionEngine
from src.audit import save_audit_log


DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "creditcard.csv"
)


df = pd.read_csv(DATA_PATH)

sample = df.drop(
    columns=["Class"]
).sample(
    n=10,
    random_state=42
)


engine = FraudDecisionEngine()

results = engine.analyze_batch(sample)


audit_data = save_audit_log(results)


print("\nDECISION RESULTS\n")

print(
    results[
        [
            "Amount",
            "Risk_Score",
            "Decision",
            "Reason"
        ]
    ].to_string()
)


print("\nAUDIT LOG CREATED\n")

print(
    audit_data.to_string(
        index=False
    )
)