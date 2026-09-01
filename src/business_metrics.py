import numpy as np


def calculate_business_metrics(y_true, y_pred, amounts):

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    amounts = np.array(amounts)

    true_positive = (y_true == 1) & (y_pred == 1)
    false_positive = (y_true == 0) & (y_pred == 1)
    false_negative = (y_true == 1) & (y_pred == 0)
    true_negative = (y_true == 0) & (y_pred == 0)

    fraud_detected_amount = amounts[true_positive].sum()
    fraud_missed_amount = amounts[false_negative].sum()

    false_positive_amount = amounts[false_positive].sum()

    metrics = {
        "true_positives": int(true_positive.sum()),
        "false_positives": int(false_positive.sum()),
        "false_negatives": int(false_negative.sum()),
        "true_negatives": int(true_negative.sum()),
        "fraud_detected_amount": float(fraud_detected_amount),
        "fraud_missed_amount": float(fraud_missed_amount),
        "false_positive_cost": float(false_positive_amount)
    }

    return metrics