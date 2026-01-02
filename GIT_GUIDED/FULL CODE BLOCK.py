import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Step 1: Load the dataset
df = pd.read_csv('PhiUSIIL_Phishing_URL_Dataset.csv')  # Use your actual filename

# Step 2: Filter African ccTLDs
african_ccTLDs = ['.ng', '.za', '.ke', '.gh', '.ug', '.tz', '.eg', '.sn', '.rw', '.dz']
african_urls = df[df['URL'].str.contains('|'.join(african_ccTLDs), na=False)]

# Step 3: Drop irrelevant columns for training
# Drop obviously non-numeric columns
drop_cols = ['FILENAME', 'URL', 'Domain', 'Title', 'label']

# Keep only numeric and boolean columns
X = african_urls.drop(columns=drop_cols)

# Drop any columns with non-numeric data types (object or string)
X = X.select_dtypes(include=['int64', 'float64', 'bool'])

# Define target
y = african_urls['label']


# Step 4: Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Step 5: Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 6: Predict and evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))



import joblib

# Save the trained model
joblib.dump(model, 'phishing_model_africa.pkl')

# Save the list of feature column names (needed for prediction)
joblib.dump(X.columns.tolist(), 'model_features.pkl')

print("✅ Model and feature list saved.")
