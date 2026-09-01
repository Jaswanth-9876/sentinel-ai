import os
from datetime import datetime

import pandas as pd


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

LOG_DIR = os.path.join(
    BASE_DIR,
    "logs"
)

LOG_PATH = os.path.join(
    LOG_DIR,
    "audit_log.csv"
)

os.makedirs(
    LOG_DIR,
    exist_ok=True
)


def get_next_transaction_id():

    if not os.path.exists(LOG_PATH):

        return 1

    audit_log = pd.read_csv(LOG_PATH)

    if audit_log.empty:

        return 1

    return int(
        audit_log["Transaction_ID"].max()
    ) + 1


def create_audit_log(results):

    audit_data = results.copy()

    start_id = get_next_transaction_id()

    audit_data.insert(
        0,
        "Timestamp",
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    audit_data.insert(
        1,
        "Transaction_ID",
        range(
            start_id,
            start_id + len(audit_data)
        )
    )

    columns = [
        "Timestamp",
        "Transaction_ID",
        "Amount",
        "Risk_Score",
        "Decision",
        "Reason"
    ]

    return audit_data[columns]


def save_audit_log(results):

    audit_data = create_audit_log(
        results
    )

    file_exists = os.path.exists(
        LOG_PATH
    )

    audit_data.to_csv(
        LOG_PATH,
        mode="a",
        index=False,
        header=not file_exists
    )

    return audit_data


def load_audit_log():

    if not os.path.exists(LOG_PATH):

        return pd.DataFrame()

    return pd.read_csv(LOG_PATH)