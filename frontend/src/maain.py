from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="PayGuard AI",
    description="AI-Powered Payment Fraud Detection API",
    version="1.0"
)

# Allow React frontend to communicate with Python backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Transaction(BaseModel):
    merchant: str
    amount: float


@app.get("/")
def home():
    return {
        "message": "Welcome to PayGuard AI Fraud Detection Engine",
        "status": "Online"
    }


@app.post("/analyze")
def analyze_transaction(transaction: Transaction):

    risk = 10
    reasons = []

    merchant = transaction.merchant.lower()
    amount = transaction.amount

    # Transaction amount analysis
    if amount > 10000:
        risk += 25
        reasons.append("High transaction amount")

    if amount > 50000:
        risk += 25
        reasons.append("Very large transaction amount")

    # Merchant analysis
    if "unknown" in merchant:
        risk += 30
        reasons.append("Unrecognized merchant indicator")

    risk = min(risk, 100)

    # Risk classification
    if risk >= 60:
        status = "Fraud Risk"
        recommendation = "Further verification recommended"

    elif risk >= 30:
        status = "Review"
        recommendation = "Review this transaction carefully"

    else:
        status = "Safe"
        recommendation = "No significant risk indicators detected"

    return {
        "merchant": transaction.merchant,
        "amount": amount,
        "risk_score": risk,
        "status": status,
        "reasons": reasons,
        "recommendation": recommendation
    }

    