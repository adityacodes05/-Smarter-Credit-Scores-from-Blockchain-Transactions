import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import joblib

# Load extracted features CSV (you should first run feature_engineering if needed)
df = pd.read_csv("features.csv")  # Make sure you have this after processing JSON

X = df[[
    "total_transactions", "num_deposit", "num_borrow", "num_repay",
    "num_liquidation", "total_usd_deposit", "total_usd_borrow",
    "total_usd_repay", "avg_tx_interval", "repay_borrow_ratio"
]].fillna(0)

# Scale data
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Train KMeans
kmeans = KMeans(n_clusters=10, random_state=42, n_init=10)
kmeans.fit(X_scaled)

# Save model and scaler
joblib.dump(kmeans, "model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("✅ model.pkl and scaler.pkl generated.")
