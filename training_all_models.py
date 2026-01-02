import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, accuracy_score

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

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# --------------------------
# 5. Define ML Models
# --------------------------
models = {
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "SVM": SVC(kernel='linear', probability=True),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=5),
    "Naive Bayes": GaussianNB(),
    "ANN (MLPClassifier)": MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=300, random_state=42)
}

# --------------------------
# 6. Train & Evaluate Models
# --------------------------
for name, model in models.items():
    print(f"\n📘 Training {name}...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print(f"✅ {name} Results:")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    if name == "Random Forest":
        joblib.dump(model, "Random_Forest TRAINED_MODEL.pkl")
        joblib.dump(X.columns.tolist(), "RandForest_model_features.pkl")
        print("💾 Random Forest model saved to: Random_Forest TRAINED_MODEL.pkl")
        print("💾 Feature list saved to: RandForest_model_features.pkl")
