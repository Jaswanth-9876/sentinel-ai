import os
import json

import pandas as pd
import streamlit as st
import requests
import plotly.express as px

from src.audit import save_audit_log, load_audit_log


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

METRICS_PATH = os.path.join(
    BASE_DIR,
    "models",
    "metrics.json"
)

API_URL = os.getenv(
    "API_URL",
    "https://sentinel-ai-6pcz.onrender.com"
)


st.set_page_config(
    page_title="SentinelAI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_data
def load_metrics():

    if not os.path.exists(METRICS_PATH):
        return None

    with open(
        METRICS_PATH,
        "r"
    ) as file:

        return json.load(file)


def check_api_health():

    try:

        response = requests.get(
            f"{API_URL}/health",
            timeout=5
        )

        return response.status_code == 200

    except requests.RequestException:

        return False


def main():

    metrics = load_metrics()

    with st.sidebar:

        st.title("🛡️ SentinelAI")

        st.caption(
            "Fraud Risk Management Platform"
        )

        st.divider()

        api_healthy = check_api_health()

        if api_healthy:

            st.success(
                "API Connected"
            )

        else:

            st.error(
                "API Offline"
            )

        st.divider()

        st.subheader("Platform")

        st.write(
            "AI-powered fraud detection "
            "with explainable risk decisions."
        )

        st.divider()

        st.caption(
            "Version 1.0.0"
        )


    st.title(
        "🛡️ SentinelAI"
    )

    st.subheader(
        "Explainable Fraud Risk Management System"
    )

    st.caption(
        "Analyze transactions, detect fraud risk, "
        "and make transparent decisions."
    )

    st.divider()


    if metrics is None:

        st.error(
            "Model metrics not found. "
            "Please run the training pipeline first."
        )

        return


    precision = metrics["precision"]
    recall = metrics["recall"]
    f1_score = metrics["f1_score"]
    best_model = metrics.get(
        "best_model",
        "Fraud Detection Model"
    )


    st.subheader(
        "Model Performance"
    )


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Precision",
        f"{precision * 100:.2f}%"
    )


    col2.metric(
        "Recall",
        f"{recall * 100:.2f}%"
    )


    col3.metric(
        "F1 Score",
        f"{f1_score * 100:.2f}%"
    )


    col4.metric(
        "Test Samples",
        metrics["test_samples"]
    )


    st.caption(
        f"Active Model: {best_model}"
    )


    st.divider()


    tab1, tab2, tab3 = st.tabs(
        [
            "🔍 Analyze Transactions",
            "📊 Business Impact",
            "📋 Audit Trail"
        ]
    )


    with tab1:

        st.header(
            "Transaction Risk Analysis"
        )

        st.write(
            "Upload a CSV file containing "
            "transactions for fraud risk analysis."
        )


        uploaded_file = st.file_uploader(
            "Upload transaction CSV",
            type=["csv"]
        )


        if uploaded_file is not None:

            try:

                uploaded_data = pd.read_csv(
                    uploaded_file
                )

                st.success(
                    f"{len(uploaded_data)} transactions loaded successfully."
                )


                with st.expander(
                    "Preview Uploaded Data",
                    expanded=False
                ):

                    st.dataframe(
                        uploaded_data.head(10),
                        use_container_width=True
                    )


                if st.button(
                    "Analyze Fraud Risk",
                    type="primary",
                    use_container_width=True
                ):

                    with st.spinner(
                        "Analyzing transactions..."
                    ):
                        API_URL = os.getenv(
                            "API_URL",
                            "https://sentinel-ai-6pcz.onrender.com"
                        )

                        response = requests.post(
                            f"{API_URL}/predict/csv",
                            files={
                                "file": (
                                    uploaded_file.name,
                                    uploaded_file.getvalue(),
                                    "text/csv"
                                )
                            },
                            timeout=60
                        )


                        response.raise_for_status()


                        api_response = response.json()


                        results = pd.DataFrame(
                            api_response["results"]
                        )
                        save_audit_log(results)


                    st.success(
                        "Fraud risk analysis completed successfully."
                    )


                    st.subheader(
                        "Risk Overview"
                    )


                    metric1, metric2, metric3, metric4 = st.columns(4)


                    metric1.metric(
                        "Total",
                        api_response[
                            "total_transactions"
                        ]
                    )


                    metric2.metric(
                        "High Risk",
                        api_response[
                            "high_risk"
                        ]
                    )


                    metric3.metric(
                        "Review",
                        api_response[
                            "review"
                        ]
                    )


                    metric4.metric(
                        "Allowed",
                        api_response[
                            "allowed"
                        ]
                    )


                    st.divider()


                    chart_col1, chart_col2 = st.columns(2)


                    with chart_col1:

                        st.subheader(
                            "Decision Distribution"
                        )


                        decision_counts = (
                            results[
                                "Decision"
                            ]
                            .value_counts()
                            .reset_index()
                        )


                        decision_counts.columns = [
                            "Decision",
                            "Count"
                        ]


                        fig_decision = px.bar(
                            decision_counts,
                            x="Decision",
                            y="Count",
                            text="Count"
                        )


                        fig_decision.update_layout(
                            height=400
                        )


                        st.plotly_chart(
                            fig_decision,
                            use_container_width=True
                        )


                    with chart_col2:

                        st.subheader(
                            "Risk Score Distribution"
                        )


                        fig_risk = px.histogram(
                            results,
                            x="Risk_Score",
                            nbins=20
                        )


                        fig_risk.update_layout(
                            height=400
                        )


                        st.plotly_chart(
                            fig_risk,
                            use_container_width=True
                        )


                    st.divider()


                    high_risk_transactions = results[
                        results["Decision"] == "HOLD"
                    ]


                    if not high_risk_transactions.empty:

                        st.subheader(
                            "🚨 High Risk Transactions"
                        )


                        high_risk_columns = [
                            "Amount",
                            "Risk_Score",
                            "Decision",
                            "Reason"
                        ]


                        st.dataframe(
                            high_risk_transactions[
                                high_risk_columns
                            ],
                            use_container_width=True
                        )


                    else:

                        st.info(
                            "No high-risk transactions were detected."
                        )


                    st.divider()


                    st.subheader(
                        "All Risk Analysis Results"
                    )


                    display_columns = [
                        "Amount",
                        "Risk_Score",
                        "Decision",
                        "Reason"
                    ]


                    st.dataframe(
                        results[
                            display_columns
                        ],
                        use_container_width=True,
                        height=400
                    )


                    csv_data = results.to_csv(
                        index=False
                    ).encode(
                        "utf-8"
                    )


                    st.download_button(
                        "Download Analysis Results",
                        csv_data,
                        "fraud_analysis_results.csv",
                        "text/csv",
                        use_container_width=True
                    )


            except requests.RequestException as error:

                st.error(
                    "Unable to connect to the SentinelAI API."
                )

                st.warning(
                    str(error)
                )


            except Exception as error:

                st.error(
                    "The uploaded file could not be analyzed."
                )

                st.warning(
                    str(error)
                )


    with tab2:

        st.header(
            "Business Impact"
        )


        st.caption(
            "Performance impact calculated "
            "on the held-out test dataset."
        )


        business = metrics[
            "business_metrics"
        ]


        col1, col2, col3 = st.columns(3)


        col1.metric(
            "Fraud Cases Detected",
            business[
                "true_positives"
            ]
        )


        col2.metric(
            "Fraud Cases Missed",
            business[
                "false_negatives"
            ]
        )


        col3.metric(
            "False Positives",
            business[
                "false_positives"
            ]
        )


        st.divider()


        col1, col2, col3 = st.columns(3)


        col1.metric(
            "Detected Amount at Risk",
            f"{business['fraud_detected_amount']:.2f}"
        )


        col2.metric(
            "Missed Fraud Amount",
            f"{business['fraud_missed_amount']:.2f}"
        )


        col3.metric(
            "False Positive Cost",
            f"{business['false_positive_cost']:.2f}"
        )


        impact_data = pd.DataFrame(
            {
                "Metric": [
                    "Detected Fraud",
                    "Missed Fraud",
                    "False Positive Cost"
                ],
                "Amount": [
                    business[
                        "fraud_detected_amount"
                    ],
                    business[
                        "fraud_missed_amount"
                    ],
                    business[
                        "false_positive_cost"
                    ]
                ]
            }
        )


        fig_business = px.bar(
            impact_data,
            x="Metric",
            y="Amount",
            text="Amount"
        )


        st.plotly_chart(
            fig_business,
            use_container_width=True
        )


        st.info(
            "Transaction amounts are shown "
            "in the dataset's original units."
        )


        with tab3:

            st.header(
                "Decision Audit Trail"
            )

            audit_log = load_audit_log()

            if audit_log.empty:

                st.info(
                    "No audit records have been created yet."
                )

            else:

              st.metric(
                  "Total Audit Records",
                  len(audit_log)
              )

              st.dataframe(
                  audit_log,
                  use_container_width=True,
                  height=500
              )

              audit_csv = audit_log.to_csv(
                  index=False
              ).encode(
                  "utf-8"
              )

              st.download_button(
                  "Download Audit Trail",
                  audit_csv,
                  "audit_log.csv",
                  "text/csv",
                  use_container_width=True
              )

if __name__ == "__main__":

    main()