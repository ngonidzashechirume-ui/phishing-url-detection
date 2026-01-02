import pandas as pd
import joblib
from sklearn.metrics import classification_report, accuracy_score

# --------------------------
# 1. Load Saved Model & Features
# --------------------------
print("📥 Loading saved model and feature list...")
model = joblib.load("Random_Forest TRAINED_MODEL.pkl")
feature_list = joblib.load("RandForest_model_features.pkl")
print("✅ Model and features loaded.")

# --------------------------
# 2. Load Dataset and Prepare Features
# --------------------------
print("📄 Loading dataset...")
df = pd.read_csv("PhiUSIIL_Phishing_URL_Dataset.csv")

# Filter African domain URLs
african_ccTLDs = ['.za', '.ng', '.ke', '.gh', '.tz', '.ug', '.bw', '.zm', '.zw', '.sn', '.cm', '.dz', '.ma', '.eg']
df = df[df['URL'].str.contains('|'.join(african_ccTLDs), na=False)]
print("🌍 Filtered African dataset shape:", df.shape)

# Clean columns
columns_to_drop = ['FILENAME', 'URL', 'Domain', 'Title']
df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')
df = df.dropna()
df = df.select_dtypes(include=['number', 'bool'])

# Split features/labels
X = df[feature_list]
y = df['label']

# --------------------------
# 3. Predict and Evaluate
# --------------------------
print("🔮 Running batch predictions...")
y_pred = model.predict(X)

print("✅ Prediction complete.\n")
print("🎯 Evaluation Results:")
print("Accuracy:", accuracy_score(y, y_pred))
print(classification_report(y, y_pred))

# --------------------------
# 4. Save Predictions to CSV
# --------------------------
output_df = pd.DataFrame({
    'Prediction': y_pred,
    'Actual Label': y.values
})
output_df.to_csv("RandForest_BatchPredictions.csv", index=False)
print("\n💾 Predictions exported to: RandForest_BatchPredictions.csv")
