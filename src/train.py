import os
import sys
import json
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from src.decision_engine import FraudDecisionEngine
from src.audit import save_audit_log, load_audit_log

METRICS_PATH = os.path.join(
    BASE_DIR,
    "models",
    "metrics.json"
)

st.set_page_config(
    page_title="SentinelAI",
    page_icon="🛡️",
    layout="wide"
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 1.8rem 2rem;
        border-radius: 16px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 1.5rem;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        opacity: 0.75;
    }

    .section-title {
        font-size: 1.6rem;
        font-weight: 650;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .policy-card {
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)


@st.cache_data
def load_metrics():
    if not os.path.exists(METRICS_PATH):
        return None

    with open(METRICS_PATH, "r") as file:
        return json.load(file)


def create_decision_chart(results):
    decision_counts = results["Decision"].value_counts()

    fig, ax = plt.subplots()

    ax.bar(
        decision_counts.index,
        decision_counts.values
    )

    ax.set_xlabel("Decision")
    ax.set_ylabel("Transactions")
    ax.set_title("Decision Distribution")

    return fig


def create_risk_distribution(results):
    fig, ax = plt.subplots()

    ax.hist(
        results["Risk_Score"],
        bins=15
    )

    ax.set_xlabel("Risk Score")
    ax.set_ylabel("Transactions")
    ax.set_title("Fraud Risk Distribution")

    return fig


def create_amount_risk_chart(results):
    fig, ax = plt.subplots()

    ax.scatter(
        results["Amount"],
        results["Risk_Score"]
    )

    ax.set_xlabel("Transaction Amount")
    ax.set_ylabel("Risk Score")
    ax.set_title("Transaction Amount vs Risk Score")

    return fig


def generate_summary(results):
    total = len(results)

    hold_count = len(
        results[
            results["Decision"] == "HOLD"
        ]
    )

    review_count = len(
        results[
            results["Decision"] == "REVIEW"
        ]
    )

    allow_count = len(
        results[
            results["Decision"] == "ALLOW"
        ]
    )

    highest_risk = results["Risk_Score"].max()

    return (
        f"{total} transactions were analyzed. "
        f"{hold_count} transactions were classified as high risk, "
        f"{review_count} transactions require review, and "
        f"{allow_count} transactions were approved. "
        f"The highest observed fraud risk score was "
        f"{highest_risk * 100:.2f}%."
    )


def main():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">🛡️ SentinelAI</div>
            <div class="hero-subtitle">
                AI-Powered Fraud Risk Intelligence for Modern Payments
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    metrics = load_metrics()

    if metrics is None:
        st.error(
            "Model metrics not found. Please run the training pipeline first."
        )
        return

    precision = metrics["precision"]
    recall = metrics["recall"]
    f1_score = metrics["f1_score"]

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

    st.divider()

    tab1, tab2, tab3 = st.tabs(
        [
            "🔍 Risk Intelligence",
            "📊 Business Impact",
            "📋 Audit Center"
        ]
    )

    with tab1:
        st.markdown(
            '<div class="section-title">Transaction Risk Analysis</div>',
            unsafe_allow_html=True
        )

        policy1, policy2, policy3 = st.columns(3)

        with policy1:
            st.markdown(
                """
                <div class="policy-card">
                    <h3>🟢 ALLOW</h3>
                    <p>Low Risk</p>
                    <p>Risk Score &lt; 40%</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with policy2:
            st.markdown(
                """
                <div class="policy-card">
                    <h3>🟡 REVIEW</h3>
                    <p>Medium Risk</p>
                    <p>40% - 75%</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with policy3:
            st.markdown(
                """
                <div class="policy-card">
                    <h3>🔴 HOLD</h3>
                    <p>High Risk</p>
                    <p>Risk Score ≥ 75%</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("")

        uploaded_file = st.file_uploader(
            "Upload transaction data",
            type=["csv"]
        )

        if uploaded_file is not None:
            try:
                uploaded_data = pd.read_csv(uploaded_file)

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

                if "Class" in uploaded_data.columns:
                    analysis_data = uploaded_data.drop(
                        columns=["Class"]
                    )
                else:
                    analysis_data = uploaded_data

                if st.button(
                    "Analyze Fraud Risk",
                    type="primary",
                    use_container_width=True
                ):
                    with st.spinner(
                        "Running AI fraud risk analysis..."
                    ):
                        engine = FraudDecisionEngine()

                        results = engine.analyze_batch(
                            analysis_data
                        )

                        save_audit_log(results)

                    st.success(
                        "Fraud risk analysis completed successfully."
                    )

                    st.session_state["results"] = results

            except Exception as error:
                st.error(
                    "The uploaded file could not be analyzed."
                )

                st.warning(str(error))

        if "results" in st.session_state:
            results = st.session_state["results"]

            total_transactions = len(results)

            hold_count = len(
                results[
                    results["Decision"] == "HOLD"
                ]
            )

            review_count = len(
                results[
                    results["Decision"] == "REVIEW"
                ]
            )

            allow_count = len(
                results[
                    results["Decision"] == "ALLOW"
                ]
            )

            st.write("")

            metric1, metric2, metric3, metric4 = st.columns(4)

            metric1.metric(
                "Transactions Analyzed",
                total_transactions
            )

            metric2.metric(
                "High Risk",
                hold_count
            )

            metric3.metric(
                "Under Review",
                review_count
            )

            metric4.metric(
                "Approved",
                allow_count
            )

            st.divider()

            st.markdown(
                '<div class="section-title">Fraud Intelligence Summary</div>',
                unsafe_allow_html=True
            )

            st.info(
                generate_summary(results)
            )

            chart1, chart2 = st.columns(2)

            with chart1:
                st.pyplot(
                    create_decision_chart(results)
                )

            with chart2:
                st.pyplot(
                    create_risk_distribution(results)
                )

            st.pyplot(
                create_amount_risk_chart(results)
            )

            st.divider()

            st.markdown(
                '<div class="section-title">Risk Analysis Results</div>',
                unsafe_allow_html=True
            )

            filter_col1, filter_col2 = st.columns(2)

            with filter_col1:
                selected_decisions = st.multiselect(
                    "Filter by Decision",
                    options=["ALLOW", "REVIEW", "HOLD"],
                    default=["ALLOW", "REVIEW", "HOLD"]
                )

            with filter_col2:
                minimum_risk = st.slider(
                    "Minimum Risk Score",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.0,
                    step=0.01
                )

            filtered_results = results[
                (
                    results["Decision"].isin(
                        selected_decisions
                    )
                )
                &
                (
                    results["Risk_Score"] >= minimum_risk
                )
            ]

            display_columns = [
                "Amount",
                "Risk_Score",
                "Decision",
                "Reason"
            ]

            st.dataframe(
                filtered_results[
                    display_columns
                ],
                use_container_width=True,
                height=450
            )

            csv_data = filtered_results.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "Download Analysis Results",
                csv_data,
                "fraud_analysis_results.csv",
                "text/csv",
                use_container_width=True
            )

            st.divider()

            high_risk_data = results[
                results["Decision"] == "HOLD"
            ]

            if not high_risk_data.empty:
                st.markdown(
                    '<div class="section-title">⚠️ Priority Transactions</div>',
                    unsafe_allow_html=True
                )

                st.dataframe(
                    high_risk_data[
                        display_columns
                    ].sort_values(
                        "Risk_Score",
                        ascending=False
                    ),
                    use_container_width=True
                )

            st.markdown(
                '<div class="section-title">Transaction Inspector</div>',
                unsafe_allow_html=True
            )

            selected_index = st.selectbox(
                "Select a transaction",
                options=results.index.tolist()
            )

            transaction = results.loc[
                selected_index
            ]

            detail1, detail2, detail3 = st.columns(3)

            detail1.metric(
                "Amount",
                f"{transaction['Amount']:.2f}"
            )

            detail2.metric(
                "Risk Score",
                f"{transaction['Risk_Score'] * 100:.2f}%"
            )

            detail3.metric(
                "Decision",
                transaction["Decision"]
            )

            st.write(
                "**AI Explanation:** "
                + transaction["Reason"]
            )

    with tab2:
        st.markdown(
            '<div class="section-title">Business Impact Analysis</div>',
            unsafe_allow_html=True
        )

        business = metrics["business_metrics"]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Fraud Cases Detected",
            business["true_positives"]
        )

        col2.metric(
            "Fraud Cases Missed",
            business["false_negatives"]
        )

        col3.metric(
            "False Positives",
            business["false_positives"]
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

        st.info(
            "Business impact metrics are calculated using the held-out test dataset."
        )

    with tab3:
        st.markdown(
            '<div class="section-title">Decision Audit Center</div>',
            unsafe_allow_html=True
        )

        audit_log = load_audit_log()

        if audit_log.empty:
            st.info(
                "No audit records have been created yet."
            )

        else:
            filter1, filter2 = st.columns(2)

            with filter1:
                decision_filter = st.multiselect(
                    "Filter Audit Decisions",
                    options=audit_log["Decision"].unique(),
                    default=audit_log["Decision"].unique()
                )

            with filter2:
                search_transaction = st.text_input(
                    "Search Transaction ID"
                )

            filtered_audit = audit_log[
                audit_log["Decision"].isin(
                    decision_filter
                )
            ]

            if search_transaction:
                filtered_audit = filtered_audit[
                    filtered_audit[
                        "Transaction_ID"
                    ].astype(str).str.contains(
                        search_transaction
                    )
                ]

            st.dataframe(
                filtered_audit,
                use_container_width=True,
                height=500
            )

            audit_csv = filtered_audit.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                "Download Audit Trail",
                audit_csv,
                "audit_log.csv",
                "text/csv",
                use_container_width=True
            )


if __name__ == "__main__":
    main()