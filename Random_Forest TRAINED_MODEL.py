import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# --------------------------
# 1. Load Dataset
# --------------------------
df = pd.read_csv("PhiUSIIL_Phishing_URL_Dataset.csv")
print("📊 Raw dataset shape:", df.shape)

# --------------------------
# 2. Filter African Domains
# --------------------------
african_ccTLDs = ['.za', '.ng', '.ke', '.gh', '.tz', '.ug', '.bw', '.zm', '.zw', '.sn', '.cm', '.dz', '.ma', '.eg']
df = df[df['URL'].str.contains('|'.join(african_ccTLDs), na=False)]
print("🌍 Filtered African URLs:", df.shape)

# --------------------------
# 3. Clean Data
# --------------------------
columns_to_drop = ['FILENAME', 'URL', 'Domain', 'Title']
df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')
df = df.dropna()
df = df.select_dtypes(include=['number', 'bool'])

# --------------------------
# 4. Feature and Label Split
# --------------------------
X = df.drop('label', axis=1)
y = df['label']

# Save column order
feature_columns = X.columns.tolist()
joblib.dump(feature_columns, 'model_features.pkl')  # ✅ Save feature names

# --------------------------
# 5. Train Random Forest Model
# --------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# --------------------------
# 6. Save Trained Model
# --------------------------
joblib.dump(model, 'phishing_model_africa.pkl')  # ✅ Save the model
print("✅ Random Forest model saved as 'phishing_model_africa.pkl'")
print("✅ Feature list saved as 'model_features.pkl'")
