# 🛡️ PayGuard AI
### AI-Powered Payment Fraud Detection System

PayGuard AI is an AI-powered payment fraud detection prototype that identifies potentially suspicious transactions using machine learning.

It analyzes transaction details, calculates a risk score between 0 and 100, classifies transactions, and provides reasons for its risk assessment.

## 🚀 Features

- AI-based transaction risk analysis.
- Random Forest machine learning model.
- Risk score from 0 to 100.
- Three transaction classifications:
  - 🟢 Safe
  - 🟡 Review
  - 🔴 Fraud Risk
- Unknown merchant detection.
- International transaction risk detection.
- High-velocity transaction detection.
- Unusual-hour transaction detection.
- Security alerts.
- Transaction history.
- Dashboard statistics.
- SQLite database integration.

## 🛠️ Technologies Used

### Frontend
- React.js
- JavaScript
- CSS
- Vite

### Backend
- Python
- FastAPI
- Uvicorn

### Machine Learning
- Scikit-learn
- Random Forest Classifier
- NumPy
- Joblib

### Database
- SQLite

## 📁 Project Structure

```text
PayGuardAI/
│
├── backend/
│   ├── main.py
│   ├── fraud_model.pkl
│   ├── train_model.py/
│   │   └── train_model.py
│   └── venv/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/darshanramesh12/PayGuardAI.git
cd PayGuardAI
```

### 2. Set Up the Backend

Open a terminal:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install fastapi uvicorn scikit-learn numpy joblib
```

### 3. Run the Backend

```powershell
python -m uvicorn main:app --reload
```

Backend URL:

http://127.0.0.1:8000

API Documentation:

http://127.0.0.1:8000/docs

### 4. Set Up the Frontend

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the frontend in your browser:

http://localhost:5174

## 🔍 How It Works

1. The user enters transaction information.
2. The system collects transaction risk indicators.
3. The Random Forest model analyzes the transaction.
4. A risk score is calculated.
5. The transaction is classified as Safe, Review, or Fraud Risk.
6. Detection reasons and recommendations are displayed.
7. Transaction information is stored in the SQLite database.

## 🧪 Sample Test Cases

| Merchant | Amount | Expected Result |
|---|---:|---|
| Amazon | ₹2,400 | Safe |
| Unknown Store | ₹85,000 | Fraud Risk |

The high-risk demonstration includes:
- International transaction enabled.
- Multiple transactions in a short time enabled.
- Unusual transaction hour enabled.

## 🎯 Project Objective

The main objective of PayGuard AI is to demonstrate how machine learning can help identify suspicious payment transactions and provide understandable risk assessments.

## 🔮 Future Enhancements

- Real-time payment monitoring.
- Improved machine learning using real-world datasets.
- Advanced fraud analytics.
- Email and SMS security notifications.
- Cloud deployment.
- Integration with payment gateways.

## ⚠️ Disclaimer

This project uses a synthetic demonstration dataset. The machine learning model is intended for educational and hackathon demonstration purposes only.

Its performance has not been validated against real-world banking fraud data. It should not be used to make actual financial decisions.

## 📌 Project Status

**Hackathon Prototype – Core Implementation Completed**

The frontend, backend, machine learning model, transaction analysis, risk classification, and transaction storage have been implemented.

## 👨‍💻 Author

**Darshan Ramesh**

GitHub: https://github.com/darshanramesh12