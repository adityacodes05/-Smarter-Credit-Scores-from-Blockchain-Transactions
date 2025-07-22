import json
import pandas as pd
from utils import extract_features

# Load the sample JSON file
with open("data/user-wallet-transactions.json", "r") as f:
    data = json.load(f)

# Extract features using utils.py
df = extract_features(data)

# Save features to CSV
df.to_csv("features.csv", index=False)
print("✅ features.csv has been created.")
