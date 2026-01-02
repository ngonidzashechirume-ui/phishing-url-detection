import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# --------------------------
# Load Model & Feature List
# --------------------------
print("📥 Loading saved model and feature list...")
model = joblib.load("Random_Forest TRAINED_MODEL.pkl")
features = joblib.load("RandForest_model_features.pkl")
print("✅ Model and features loaded.")

# --------------------------
# Load and Prepare Dataset
# --------------------------
print("📄 Loading dataset...")
df = pd.read_csv("PhiUSIIL_Phishing_URL_Dataset.csv")

# Filter African ccTLDs
african_ccTLDs = ['.za', '.ng', '.ke', '.gh', '.tz', '.ug', '.bw', '.zm', '.zw', '.sn', '.cm', '.dz', '.ma', '.eg']
df = df[df['URL'].str.contains('|'.join(african_ccTLDs), na=False)]
print("🌍 Filtered African dataset shape:", df.shape)

# Clean columns
df = df.drop(columns=[col for col in ['FILENAME', 'URL', 'Domain', 'Title'] if col in df.columns], errors='ignore')
df = df.dropna()
df = df.select_dtypes(include=['number', 'bool'])

# Prepare input/output
X = df[features]
y_true = df['label']
y_pred = model.predict(X)

# --------------------------
# Confusion Matrix
# --------------------------
print("📊 Plotting confusion matrix...")
cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Legit", "Phishing"], yticklabels=["Legit", "Phishing"])
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()

# --------------------------
# Classification Report Heatmap
# --------------------------
print("📊 Plotting classification report heatmap...")
report = classification_report(y_true, y_pred, output_dict=True)
df_report = pd.DataFrame(report).iloc[:-1, :-1]  # remove 'accuracy' and 'support'

plt.figure(figsize=(8, 4))
sns.heatmap(df_report, annot=True, cmap="YlGnBu")
plt.title("Classification Report (Heatmap)")
plt.tight_layout()
plt.show()

# --------------------------
# Feature Importance
# --------------------------
print("📊 Plotting feature importance...")
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]
top_features = [features[i] for i in indices[:10]]  # Top 10
top_importances = importances[indices[:10]]

plt.figure(figsize=(10, 5))
sns.barplot(x=top_importances, y=top_features, palette="viridis")
plt.title("Top 10 Feature Importances (Random Forest)")
plt.xlabel("Importance Score")
plt.ylabel("Feature")
plt.tight_layout()
plt.show()
