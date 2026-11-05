# PayGuard AI 🛡️
### AI-Powered Payment Fraud Detection System

PayGuard AI is an AI-powered payment fraud detection prototype designed to identify potentially suspicious transactions using machine learning and risk analysis.

The system analyzes transaction details, calculates a risk score between 0 and 100, classifies the transaction, and provides reasons for its risk assessment.

## 🚀 Features

- AI-based transaction risk analysis.
- Random Forest machine learning model.
- Risk score from 0 to 100.
- Three transaction classifications:
  - Safe
  - Review
  - Fraud Risk
- Detection of suspicious merchants.
- International transaction risk checks.
- High-velocity transaction checks.
- Unusual-hour transaction checks.
- Security alerts.
- Transaction history.
- Dashboard statistics.
- SQLite database integration.

## 🛠️ Technologies Used

**Frontend**
- React.js
- JavaScript
- CSS
- Vite

**Backend**
- Python
- FastAPI
- Uvicorn

**Machine Learning**
- Scikit-learn
- Random Forest Classifier
- NumPy
- Joblib

**Database**
- SQLite

## 📁 Project Structure

```text
PayGuardAI/
│
├── backend/
│   ├── main.py
│   ├── fraud_model.pkl
│   ├── payguard.db
│   ├── train_model.py/
│   │   └── train_model.py
│   └── venv/
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   ├── package.json
│   └── index.html
│
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd PayGuardAI
```

### 2. Start the Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install fastapi uvicorn scikit-learn numpy joblib
python -m uvicorn main:app --reload
```

Backend URL:

http://127.0.0.1:8000

API Documentation:

http://127.0.0.1:8000/docs

### 3. Start the Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the frontend:

http://localhost:5174

## 🔍 How It Works

1. The user enters transaction information.
2. The system extracts transaction risk indicators.
3. The Random Forest model analyzes the transaction.
4. A risk score is calculated.
5. The transaction is classified as Safe, Review, or Fraud Risk.
6. Detection reasons and recommendations are displayed.
7. Transaction information is stored in SQLite.

## 🧪 Sample Test Cases

| Merchant | Amount | Expected Result |
|---|---:|---|
| Amazon | ₹2,400 | Safe |
| Unknown Store | ₹85,000 | Fraud Risk |

The high-risk demonstration includes international, high-velocity, and unusual-hour indicators.

## 🎯 Project Objective

The main objective of PayGuard AI is to demonstrate how machine learning can support payment fraud detection by identifying suspicious transaction patterns and providing understandable risk assessments.

## ⚠️ Disclaimer

This project uses a synthetic demonstration dataset. Its machine learning model is intended for educational and hackathon demonstration purposes only.

It has not been validated against real-world banking fraud data and should not be used for actual financial decisions.

## 👨‍💻 Project Status

Hackathon prototype – Core fraud detection, backend integration, frontend dashboard, and transaction storage implemented.

Further improvements and deployment are planned.