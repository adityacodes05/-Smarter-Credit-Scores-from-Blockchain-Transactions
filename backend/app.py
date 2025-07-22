from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import json
import pandas as pd
from utils import extract_features
from waitress import serve
import logging

# Suppress waitress logs if desired
logging.getLogger('waitress').setLevel(logging.ERROR)

app = Flask(__name__)
CORS(app)

# Load model and scaler
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

@app.route('/')
def home():
    return '✅ Flask backend is running. Use POST /predict to upload a .json file.'

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        try:
            data = json.load(file)
        except Exception:
            return jsonify({"error": "Invalid JSON format"}), 400

        # Extract features
        df_features = extract_features(data)

        # Select required features
        required_features = [
            "total_transactions", "num_deposit", "num_borrow", "num_repay",
            "num_liquidation", "total_usd_deposit", "total_usd_borrow",
            "total_usd_repay", "avg_tx_interval", "repay_borrow_ratio"
        ]
        model_input = df_features[required_features].fillna(0)

        # Scale + predict
        scaled = scaler.transform(model_input)
        labels = model.predict(scaled)

        # Credit score mapping
        max_cluster = model.n_clusters - 1
        scores = (1000 * (max_cluster - labels) / max_cluster).astype(int)

        df_features['score'] = scores
        output = df_features[['wallet', 'score']].to_dict(orient='records')

        return jsonify(output)

    except Exception as e:
        print(f"🔥 Internal Server Error: {e}")
        return jsonify({"error": "Server error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Serving on http://localhost:5000")
    serve(app, host='0.0.0.0', port=5000)
