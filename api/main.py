import os
import sys
from io import StringIO
from typing import Dict, Any

import pandas as pd
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(BASE_DIR)

from src.decision_engine import FraudDecisionEngine
from src.audit import save_audit_log


app = FastAPI(
    title="SentinelAI Fraud Detection API",
    description="Explainable fraud risk scoring and decision API",
    version="1.0.0"
)


MAX_BATCH_SIZE = 1000


class TransactionRequest(BaseModel):

    transaction: Dict[str, Any]


@app.get("/")
def root():

    return {
        "service": "SentinelAI",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


@app.post("/predict")
def predict_fraud(
    request: TransactionRequest
):

    try:

        transaction_data = pd.DataFrame(
            [request.transaction]
        )

        engine = FraudDecisionEngine()

        results = engine.analyze_batch(
            transaction_data
        )

        save_audit_log(results)

        result = results.iloc[0]

        return {
            "risk_score": float(
                result["Risk_Score"]
            ),
            "decision": result["Decision"],
            "reason": result["Reason"]
        }

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Unable to analyze the transaction."
        )


@app.post("/predict/csv")
async def predict_csv(
    file: UploadFile = File(...)
):

    if not file.filename or not file.filename.lower().endswith(".csv"):

        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported."
        )

    try:

        contents = await file.read()

        if not contents:

            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty."
            )

        csv_text = contents.decode("utf-8")

        transaction_data = pd.read_csv(
            StringIO(csv_text)
        )

        if transaction_data.empty:

            raise HTTPException(
                status_code=400,
                detail="The uploaded CSV file contains no transactions."
            )

        if len(transaction_data) > MAX_BATCH_SIZE:

            raise HTTPException(
                status_code=400,
                detail=(
                    f"Maximum batch size is "
                    f"{MAX_BATCH_SIZE} transactions."
                )
            )

        if "Class" in transaction_data.columns:

            transaction_data = transaction_data.drop(
                columns=["Class"]
            )

        engine = FraudDecisionEngine()

        results = engine.analyze_batch(
            transaction_data
        )

        save_audit_log(results)

        hold_count = int(
            (
                results["Decision"] == "HOLD"
            ).sum()
        )

        review_count = int(
            (
                results["Decision"] == "REVIEW"
            ).sum()
        )

        allow_count = int(
            (
                results["Decision"] == "ALLOW"
            ).sum()
        )

        return {
            "total_transactions": int(
                len(results)
            ),
            "high_risk": hold_count,
            "review": review_count,
            "allowed": allow_count,
            "results": results.to_dict(
                orient="records"
            )
        }

    except HTTPException:

        raise

    except UnicodeDecodeError:

        raise HTTPException(
            status_code=400,
            detail="The CSV file must be UTF-8 encoded."
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Unable to process the uploaded CSV file."
        )