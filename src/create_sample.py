import os
import pandas as pd

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "creditcard.csv"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "sample_transactions.csv"
)

df = pd.read_csv(DATA_PATH)

fraud = df[df["Class"] == 1].sample(
    n=10,
    random_state=42
)

normal = df[df["Class"] == 0].sample(
    n=40,
    random_state=42
)

sample = pd.concat(
    [fraud, normal]
)

sample = sample.sample(
    frac=1,
    random_state=42
)

sample.to_csv(
    OUTPUT_PATH,
    index=False
)

print(
    f"Sample dataset created successfully: {OUTPUT_PATH}"
)

print(
    f"Total transactions: {len(sample)}"
)

print(
    "\nClass distribution:"
)

print(
    sample["Class"].value_counts()
)