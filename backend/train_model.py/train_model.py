import os
import numpy as np
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score
)

# Reproducible dataset
np.random.seed(42)

print("Generating PayGuard AI training dataset...")

number_of_transactions = 20000

# Generate transaction features
amount = np.random.uniform(100, 100000, number_of_transactions)

merchant_risk = np.random.randint(0, 2, number_of_transactions)
international = np.random.randint(0, 2, number_of_transactions)
high_velocity = np.random.randint(0, 2, number_of_transactions)
unusual_hour = np.random.randint(0, 2, number_of_transactions)

# Create transaction features
X = np.column_stack((
    amount,
    merchant_risk,
    international,
    high_velocity,
    unusual_hour
))

# Generate synthetic risk scores
risk_score = (
    3
    + np.where(amount > 50000, 35, 0)
    + np.where(amount > 25000, 20, 0)
    + np.where(amount > 10000, 10, 0)
    + merchant_risk * 35
    + international * 15
    + high_velocity * 25
    + unusual_hour * 10
)

# Generate labels with small noise
y = (risk_score >= 50).astype(int)

noise = np.random.random(number_of_transactions) < 0.04
y[noise] = 1 - y[noise]

print("Dataset generated successfully!")

print("Total transactions:", number_of_transactions)
print("Fraudulent examples:", int(np.sum(y)))
print("Safe examples:", int(number_of_transactions - np.sum(y)))

# Split training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Create Random Forest model
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1
)

# Train model
print("\nTraining PayGuard AI model...")

model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)[:, 1]

print("\nMODEL EVALUATION")

print("\nAccuracy:")
print(accuracy_score(y_test, predictions))

print("\nROC-AUC:")
print(roc_auc_score(y_test, probabilities))

print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

# Feature importance
feature_names = [
    "Transaction Amount",
    "Merchant Risk",
    "International",
    "High Velocity",
    "Unusual Hour"
]

print("\nFeature Importance:")

for name, importance in zip(
    feature_names,
    model.feature_importances_
):
    print(f"{name}: {importance:.4f}")

# Save model in backend folder
backend_directory = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

model_path = os.path.join(
    backend_directory,
    "fraud_model.pkl"
)

joblib.dump(model, model_path)

print("\nModel saved successfully!")
print("Location:", model_path)
