# 🛡️ SentinelAI

An AI-powered fraud risk management platform that analyzes financial transactions, detects potential fraud, and provides explainable risk decisions.

---

## 🚀 Live Demo

### 🌐 Frontend Application

🔗 https://sentinel-ai-fraud.streamlit.app/

### ⚡ Backend API

🔗 https://sentinel-ai-6pcz.onrender.com

### 📚 API Documentation

🔗 https://sentinel-ai-6pcz.onrender.com/docs

---

## 📌 Project Overview

SentinelAI is an end-to-end AI-powered fraud detection platform designed to analyze financial transactions and identify potentially fraudulent activity.

The platform uses a machine learning model to calculate fraud risk scores and provides explainable decisions for each transaction.

The system supports:

- Transaction fraud risk analysis
- Machine learning-based fraud prediction
- Explainable fraud decisions
- High-risk transaction identification
- Business impact analysis
- Decision audit trails
- Downloadable audit records

---

## ✨ Features

### 🔍 Transaction Analysis

Users can upload transaction data in CSV format.

The system analyzes transactions and assigns:

- Fraud risk score
- Fraud decision
- Explanation for the decision

### 🤖 Machine Learning Model

SentinelAI uses a trained Random Forest model for fraud detection.

The model analyzes transaction patterns and predicts the probability of fraudulent activity.

### 📊 Business Impact Dashboard

The platform provides insights into:

- Total transactions analyzed
- High-risk transactions
- Transactions requiring review
- Allowed transactions
- Fraud risk distribution

### 🚨 High-Risk Transaction Detection

Transactions identified as high risk are highlighted for further verification.

Each transaction includes an explanation describing why the decision was made.

### 📋 Decision Audit Trail

Every fraud analysis decision is recorded in an audit log.

The audit trail includes:

- Timestamp
- Transaction ID
- Transaction amount
- Risk score
- Decision
- Explanation

Users can also download the audit trail as a CSV file.

---

## 🏗️ System Architecture

```text
Transaction CSV
       │
       ▼
Streamlit Frontend
       │
       ▼
FastAPI Backend
       │
       ▼
Random Forest Model
       │
       ▼
Fraud Risk Score
       │
       ▼
Decision Engine
       │
       ▼
Audit Trail & Business Insights


🛠️ Technology Stack
Frontend
Streamlit
Pandas
Matplotlib
Backend
FastAPI
Uvicorn
Machine Learning
Scikit-learn
Random Forest
Data Processing
Pandas
NumPy
Deployment
Streamlit Community Cloud
Render
📂 Project Structure
sentinel-ai/
│
├── api/
│   └── main.py
│
├── data/
│   ├── creditcard.csv
│   └── sample_transactions.csv
│
├── logs/
│   └── audit_log.csv
│
├── models/
│   ├── fraud_model.pkl
│   └── metrics.json
│
├── src/
│   ├── audit.py
│   ├── business_metrics.py
│   ├── create_sample.py
│   ├── decision_engine.py
│   ├── test_engine.py
│   └── train.py
│
├── app.py
├── requirements.txt
└── README.md
⚙️ How It Works
Step 1: Upload Transactions

Users upload a CSV file containing transaction data.

Step 2: Fraud Prediction

The machine learning model analyzes each transaction and calculates a fraud probability.

Step 3: Risk Decision

The decision engine categorizes transactions based on their risk score.

Possible decisions include:

ALLOW
HOLD
REVIEW
Step 4: Explanation

Each decision includes a human-readable explanation.

Example:

High predicted fraud probability. Transaction should be held for verification.

Step 5: Audit Logging

All decisions are stored in an audit trail with timestamps and transaction IDs.

🧠 Model Performance
Metric	Score
Precision	90.59%
Recall	78.57%
F1 Score	84.15%

Active Model: Random Forest

Test Samples: 56,962

💻 Running Locally
1. Clone the repository
git clone https://github.com/Jaswanth-9876/sentinel-ai.git
cd sentinel-ai
2. Create a virtual environment
python -m venv venv
3. Activate the environment
Windows
venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt
5. Run the backend
uvicorn api.main:app --reload
6. Run the frontend

Open another terminal and run:

streamlit run app.py