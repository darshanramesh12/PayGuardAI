import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [amount, setAmount] = useState("");
  const [merchant, setMerchant] = useState("");
  const [international, setInternational] = useState(false);
  const [highVelocity, setHighVelocity] = useState(false);
  const [unusualHour, setUnusualHour] = useState(false);

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [transactions, setTransactions] = useState([]);

  // Load transactions from SQLite
  async function loadTransactions() {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/transactions"
      );

      if (!response.ok) {
        throw new Error("Failed to load transaction history.");
      }

      const data = await response.json();

      const savedTransactions = data.map(item => ({
        id: item.id,
        merchant: item.merchant,
        amount: item.amount,
        risk: item.risk_score,
        status: item.status,
        date: item.created_at
      }));

      setTransactions(savedTransactions);

    } catch (error) {
      console.error("History loading error:", error);
      setError("Unable to load transaction history.");
    }
  }

  useEffect(() => {
    loadTransactions();
  }, []);

  // Analyze Transaction
  async function analyzeTransaction(e) {
    e.preventDefault();

    const value = Number(amount);

    if (!merchant.trim() || !value || value <= 0) {
      setError("Please enter a valid merchant name and amount.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/analyze",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            merchant: merchant.trim(),
            amount: value,
            international: international,
            high_velocity: highVelocity,
            unusual_hour: unusualHour
          })
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.detail || `Backend error: ${response.status}`
        );
      }

      const data = await response.json();

      const newTransaction = {
        merchant: data.merchant,
        amount: data.amount,
        risk: data.risk_score,
        status: data.status
      };

      if (typeof newTransaction.risk !== "number") {
        throw new Error("Invalid risk score received from backend.");
      }

      setResult({
        ...newTransaction,
        reasons: data.reasons || [],
        recommendation:
          data.recommendation || "No recommendation provided."
      });

      await loadTransactions();

      // Clear form
      setAmount("");
      setMerchant("");
      setInternational(false);
      setHighVelocity(false);
      setUnusualHour(false);

    } catch (error) {
      console.error("Analysis error:", error);
      setError(error.message || "Backend connection failed.");
    } finally {
      setLoading(false);
    }
  }

  // Dashboard Statistics
  const safeCount = transactions.filter(
    t => t.status === "Safe"
  ).length;

  const riskyCount = transactions.filter(
    t => t.status === "Fraud Risk"
  ).length;

  const reviewCount = transactions.filter(
    t => t.status === "Review"
  ).length;

  const alertTransactions = transactions.filter(
    t => t.status === "Fraud Risk" || t.status === "Review"
  );

  const total = transactions.length;

  // Analytics Percentages
  const safePercentage = total
    ? Math.round((safeCount / total) * 100)
    : 0;

  const reviewPercentage = total
    ? Math.round((reviewCount / total) * 100)
    : 0;

  const fraudPercentage = total
    ? Math.round((riskyCount / total) * 100)
    : 0;

  return (
    <div className="app">

      {/* Sidebar */}
      <aside className="sidebar">
        <h2>🛡 PayGuard <span>AI</span></h2>
        <p className="tagline">INTELLIGENT SECURITY</p>

        <nav>
          <a className="active" href="#">▦ Dashboard</a>
          <a href="#analyzer">⌕ Transaction Analyzer</a>
          <a href="#history">▤ Transaction History</a>
          <a href="#security">◈ Security Center</a>
          <a href="#analytics">📊 Analytics</a>
        </nav>

        <div className="sidebar-bottom">
          <span className="dot"></span>
          Protection Active
        </div>
      </aside>

      {/* Main Dashboard */}
      <main className="main">

        <header>
          <div>
            <small>OVERVIEW / DASHBOARD</small>
            <h1>Security Dashboard</h1>
          </div>
          <div className="admin">PG &nbsp; Admin</div>
        </header>

        {/* Welcome */}
        <section className="welcome">
          <div>
            <h2>Welcome to PayGuard AI 👋</h2>
            <p>Monitor transactions. Detect threats. Protect payments.</p>
          </div>
          <span>● SYSTEM ONLINE</span>
        </section>

        {/* Security Alerts */}
        <section className="card" id="security">
          <h2>🚨 Security Alerts</h2>
          <p>Suspicious transaction monitoring and risk notifications.</p>

          <div className="alert-summary">
            <strong>{alertTransactions.length}</strong>
            <span>Active Alerts</span>
          </div>

          {alertTransactions.length > 0 ? (
            alertTransactions.map(transaction => (
              <div key={transaction.id} className="result">
                <h3>
                  {transaction.status === "Fraud Risk"
                    ? "🚨 High Risk Transaction"
                    : "⚠️ Transaction Needs Review"}
                </h3>

                <p>
                  <strong>Merchant:</strong> {transaction.merchant}
                </p>

                <p>
                  <strong>Amount:</strong>{" "}
                  ₹{Number(transaction.amount).toLocaleString("en-IN")}
                </p>

                <p>
                  <strong>Risk Score:</strong> {transaction.risk}/100
                </p>

                <p>
                  <strong>Status:</strong> {transaction.status}
                </p>
              </div>
            ))
          ) : (
            <p>✅ No suspicious transactions detected.</p>
          )}
        </section>

        {/* Statistics */}
        <section className="stats">

          <div className="card">
            <p>Total Transactions</p>
            <h2>{total}</h2>
            <small>Analyzed transactions</small>
          </div>

          <div className="card">
            <p>Safe Transactions</p>
            <h2 className="green">{safeCount}</h2>
            <small>Low-risk transactions</small>
          </div>

          <div className="card">
            <p>Fraud Alerts</p>
            <h2 className="red">{riskyCount}</h2>
            <small>High-risk transactions</small>
          </div>

          <div className="card">
            <p>Needs Review</p>
            <h2>{reviewCount}</h2>
            <small>Transactions requiring review</small>
          </div>

        </section>

        {/* Transaction Analytics */}
        <section className="card analytics" id="analytics">
          <h2>📊 Transaction Analytics</h2>
          <p>Overview of analyzed transaction risk levels.</p>

          <div className="analytics-item">
            <div className="analytics-label">
              <span>🟢 Safe Transactions</span>
              <strong>{safePercentage}%</strong>
            </div>

            <div className="analytics-bar">
              <div
                className="analytics-fill safe-fill"
                style={{ width: `${safePercentage}%` }}
              ></div>
            </div>

            <small>{safeCount} transactions</small>
          </div>

          <div className="analytics-item">
            <div className="analytics-label">
              <span>🟡 Review Transactions</span>
              <strong>{reviewPercentage}%</strong>
            </div>

            <div className="analytics-bar">
              <div
                className="analytics-fill review-fill"
                style={{ width: `${reviewPercentage}%` }}
              ></div>
            </div>

            <small>{reviewCount} transactions</small>
          </div>

          <div className="analytics-item">
            <div className="analytics-label">
              <span>🔴 Fraud Risk Transactions</span>
              <strong>{fraudPercentage}%</strong>
            </div>

            <div className="analytics-bar">
              <div
                className="analytics-fill fraud-fill"
                style={{ width: `${fraudPercentage}%` }}
              ></div>
            </div>

            <small>{riskyCount} transactions</small>
          </div>
        </section>

        {/* Transaction Analyzer */}
        <section className="analyzer card" id="analyzer">
          <h2>🔍 Transaction Analyzer</h2>
          <p>Enter transaction details to evaluate its risk.</p>

          <form onSubmit={analyzeTransaction}>

            <div>
              <label>Merchant Name</label>
              <input
                type="text"
                placeholder="Enter merchant name"
                value={merchant}
                onChange={e => setMerchant(e.target.value)}
              />
            </div>

            <div>
              <label>Transaction Amount (₹)</label>
              <input
                type="number"
                min="0.01"
                step="0.01"
                placeholder="Enter amount"
                value={amount}
                onChange={e => setAmount(e.target.value)}
              />
            </div>

            {/* Additional ML Features */}
            <div className="risk-inputs">
              <h3>Additional Security Checks</h3>
              <p>Select the conditions that apply to this transaction.</p>

              <label className="risk-checkbox">
                <input
                  type="checkbox"
                  checked={international}
                  onChange={e => setInternational(e.target.checked)}
                />
                <span>🌍 International Transaction</span>
              </label>

              <label className="risk-checkbox">
                <input
                  type="checkbox"
                  checked={highVelocity}
                  onChange={e => setHighVelocity(e.target.checked)}
                />
                <span>⚡ Multiple Transactions in a Short Time</span>
              </label>

              <label className="risk-checkbox">
                <input
                  type="checkbox"
                  checked={unusualHour}
                  onChange={e => setUnusualHour(e.target.checked)}
                />
                <span>🕒 Transaction at an Unusual Hour</span>
              </label>
            </div>

            <button type="submit" disabled={loading}>
              {loading ? "Analyzing..." : "Analyze Transaction →"}
            </button>

          </form>

          {error && (
            <p className="error-message">{error}</p>
          )}

          {/* Analysis Result */}
          {result && (
            <div className="result">
              <h3>Analysis Result</h3>

              <p>
                <strong>Merchant:</strong> {result.merchant}
              </p>

              <p>
                <strong>Amount:</strong>{" "}
                ₹{Number(result.amount).toLocaleString("en-IN")}
              </p>

              <p>
                <strong>Risk Score:</strong> {result.risk}/100
              </p>

              <p>
                <strong>Status:</strong> {result.status}
              </p>

              <h4>Detection Reasons</h4>

              {result.reasons.length > 0 ? (
                <ul>
                  {result.reasons.map((reason, index) => (
                    <li key={index}>{reason}</li>
                  ))}
                </ul>
              ) : (
                <p>No significant risk indicators detected.</p>
              )}

              <p>
                <strong>Recommendation:</strong>{" "}
                {result.recommendation}
              </p>
            </div>
          )}
        </section>

        {/* Transaction History */}
        <section className="card history" id="history">
          <h2>Recent Transactions</h2>

          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>MERCHANT</th>
                  <th>AMOUNT</th>
                  <th>RISK SCORE</th>
                  <th>STATUS</th>
                </tr>
              </thead>

              <tbody>
                {transactions.length > 0 ? (
                  transactions.map(t => (
                    <tr key={t.id}>
                      <td>{t.merchant}</td>

                      <td>
                        ₹{Number(t.amount).toLocaleString("en-IN")}
                      </td>

                      <td>{t.risk}/100</td>

                      <td>
                        <span className={`badge ${
                          t.status === "Safe" ? "safe" :
                          t.status === "Review" ? "review" : "danger"
                        }`}>
                          {t.status}
                        </span>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="4">No transactions available yet.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>

        {/* Footer */}
        <footer>
          © 2026 PayGuard AI | Intelligent Payment Security
        </footer>

      </main>
    </div>
  );
}

export default App;
