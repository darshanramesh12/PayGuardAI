import os
import sqlite3
import joblib

from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# --------------------------------
# APPLICATION SETUP
# --------------------------------

app = FastAPI(
    title="PayGuard AI",
    description="AI-powered Payment Fraud Detection System",
    version="2.0"
)


# --------------------------------
# CORS CONFIGURATION
# --------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------
# MODEL AND DATABASE PATHS
# --------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "fraud_model.pkl")

DB_PATH = os.path.join(BASE_DIR, "payguard.db")


# --------------------------------
# LOAD TRAINED ML MODEL
# --------------------------------

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Trained model not found: {MODEL_PATH}"
    )

model = joblib.load(MODEL_PATH)

print("PayGuard AI model loaded successfully!")


# --------------------------------
# DATABASE INITIALIZATION
# --------------------------------

def init_db():

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            merchant TEXT NOT NULL,

            amount REAL NOT NULL,

            risk_score INTEGER NOT NULL,

            status TEXT NOT NULL,

            created_at TEXT NOT NULL

        )
    """)

    connection.commit()

    connection.close()


init_db()

print("PayGuard AI database initialized!")


# --------------------------------
# TRANSACTION INPUT MODEL
# --------------------------------

class Transaction(BaseModel):

    merchant: str = Field(min_length=1, max_length=100)

    amount: float = Field(gt=0)

    international: bool = False

    high_velocity: bool = False

    unusual_hour: bool = False


# --------------------------------
# HOME API
# --------------------------------

@app.get("/")
def home():

    return {
        "message": "Welcome to PayGuard AI",
        "status": "Running",
        "model": "Random Forest Classifier",
        "version": "2.0"
    }


# --------------------------------
# HEALTH CHECK API
# --------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "database": "connected"
    }


# --------------------------------
# FRAUD ANALYSIS API
# --------------------------------

@app.post("/analyze")
def analyze_transaction(transaction: Transaction):

    try:

        # Merchant risk detection
        merchant_name = transaction.merchant.strip()

        if not merchant_name:
            raise HTTPException(
                status_code=400,
                detail="Merchant name cannot be empty"
            )

        merchant_risk = int(
            "unknown" in merchant_name.lower()
        )

        # Prepare all five ML features
        features = [[

            transaction.amount,

            merchant_risk,

            int(transaction.international),

            int(transaction.high_velocity),

            int(transaction.unusual_hour)

        ]]

        # Predict fraud probability
        probability = model.predict_proba(features)[0][1]

        risk_score = round(probability * 100)

        # Determine transaction status
        if risk_score >= 60:

            status = "Fraud Risk"

        elif risk_score >= 30:

            status = "Review"

        else:

            status = "Safe"

        # Generate detection reasons
        reasons = []

        if transaction.amount > 10000:
            reasons.append("High transaction amount")

        if merchant_risk:
            reasons.append("Unknown merchant detected")

        if transaction.international:
            reasons.append("International transaction")

        if transaction.high_velocity:
            reasons.append("Multiple transactions detected in a short period")

        if transaction.unusual_hour:
            reasons.append("Transaction made at an unusual hour")

        if not reasons:
            reasons.append("No obvious risk indicators detected")

        # Generate recommendation
        if status == "Fraud Risk":

            recommendation = (
                "High risk detected. Block or verify this transaction "
                "before proceeding."
            )

        elif status == "Review":

            recommendation = (
                "Transaction requires additional verification."
            )

        else:

            recommendation = (
                "Transaction appears safe based on the model prediction."
            )

        # Save transaction in SQLite
        connection = sqlite3.connect(DB_PATH)

        cursor = connection.cursor()

        cursor.execute("""

            INSERT INTO transactions
            (merchant, amount, risk_score, status, created_at)

            VALUES (?, ?, ?, ?, ?)

        """, (

            merchant_name,

            transaction.amount,

            risk_score,

            status,

            datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        ))

        connection.commit()

        connection.close()

        # Return analysis result
        return {

            "merchant": merchant_name,

            "amount": transaction.amount,

            "risk_score": risk_score,

            "status": status,

            "reasons": reasons,

            "recommendation": recommendation,

            "features": {

                "merchant_risk": merchant_risk,

                "international": transaction.international,

                "high_velocity": transaction.high_velocity,

                "unusual_hour": transaction.unusual_hour

            }

        }

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Transaction analysis failed: {str(error)}"
        )


# --------------------------------
# TRANSACTION HISTORY API
# --------------------------------

@app.get("/transactions")
def get_transactions():

    try:

        connection = sqlite3.connect(DB_PATH)

        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute("""

            SELECT *
            FROM transactions
            ORDER BY id DESC

        """)

        transactions = cursor.fetchall()

        connection.close()

        return [

            dict(transaction)

            for transaction in transactions

        ]

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Could not retrieve transactions: {str(error)}"
        )


# --------------------------------
# DASHBOARD STATISTICS API
# --------------------------------

@app.get("/stats")
def get_stats():

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM transactions")

    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM transactions
        WHERE status = 'Safe'
    """)

    safe = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM transactions
        WHERE status = 'Fraud Risk'
    """)

    fraud = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM transactions
        WHERE status = 'Review'
    """)

    review = cursor.fetchone()[0]

    connection.close()

    return {

        "total": total,

        "safe": safe,

        "fraud": fraud,

        "review": review

    }
