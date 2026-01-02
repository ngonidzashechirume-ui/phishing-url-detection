# Test Script for Random Forest Model Prediction on African Phishing URLs
# ------------------------------------------------------------
# Loads the trained Random Forest model and feature list,
# Prepares a sample input from the filtered African dataset,
# and outputs a prediction (Phishing or Legitimate)

import pandas as pd
import joblib

# --------------------------
# 1. Load Model and Features
# --------------------------
print("📥 Loading saved model and features...")
model = joblib.load("Random_Forest TRAINED_MODEL.pkl")
feature_list = joblib.load("RandForest_model_features.pkl")
print("✅ Model and feature list loaded successfully.")

# --------------------------
# 2. Load and Prepare Dataset
# --------------------------
print("📄 Loading dataset and preparing sample input...")
df = pd.read_csv("PhiUSIIL_Phishing_URL_Dataset.csv")

# Filter African URLs
african_ccTLDs = ['.za', '.ng', '.ke', '.gh', '.tz', '.ug', '.bw', '.zm', '.zw', '.sn', '.cm', '.dz', '.ma', '.eg']
df = df[df['URL'].str.contains('|'.join(african_ccTLDs), na=False)]

# Drop unnecessary columns
columns_to_drop = ['FILENAME', 'URL', 'Domain', 'Title']
df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')

# Drop missing values and keep only numeric/bool
df = df.dropna()
df = df.select_dtypes(include=['number', 'bool'])

# Prepare a single input sample
sample = df[feature_list].iloc[0:1]
print("✅ Sample input prepared successfully.")

# --------------------------
# 3. Make Prediction
# --------------------------
print("🔮 Making prediction...")
prediction = model.predict(sample)[0]
label = "Legitimate" if prediction == 0 else "Phishing"
print(f"\n🎯 Prediction Result: {prediction} → {label}")
