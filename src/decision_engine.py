import os
import joblib
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "fraud_model.pkl"
)


class FraudDecisionEngine:

    def __init__(
        self,
        review_threshold=0.40,
        hold_threshold=0.75
    ):

        self.review_threshold = review_threshold
        self.hold_threshold = hold_threshold

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                "Fraud model not found. Please train the model first."
            )

        self.model = joblib.load(MODEL_PATH)

        self.required_features = [
            "Time"
        ] + [
            f"V{i}" for i in range(1, 29)
        ] + [
            "Amount"
        ]

    def validate_input(self, dataframe):

        missing_columns = [
            column
            for column in self.required_features
            if column not in dataframe.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

        return True

    def get_decision(self, risk_score):

        if risk_score >= self.hold_threshold:
            return "HOLD"

        elif risk_score >= self.review_threshold:
            return "REVIEW"

        return "ALLOW"

    def get_reason(self, risk_score, decision):

        if decision == "HOLD":
            return (
                f"High predicted fraud probability "
                f"({risk_score:.2%}). "
                f"Transaction should be held for verification."
            )

        elif decision == "REVIEW":
            return (
                f"Moderate predicted fraud probability "
                f"({risk_score:.2%}). "
                f"Transaction should be reviewed."
            )

        return (
            f"Low predicted fraud probability "
            f"({risk_score:.2%}). "
            f"Transaction can proceed."
        )

    def analyze_batch(self, dataframe):

        self.validate_input(dataframe)

        features = dataframe[
            self.required_features
        ]

        probabilities = self.model.predict_proba(
            features
        )[:, 1]

        results = dataframe.copy()

        results["Risk_Score"] = probabilities

        results["Decision"] = results[
            "Risk_Score"
        ].apply(
            self.get_decision
        )

        results["Reason"] = results.apply(
            lambda row: self.get_reason(
                row["Risk_Score"],
                row["Decision"]
            ),
            axis=1
        )

        return results