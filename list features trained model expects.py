import joblib

features = joblib.load("RandForest_model_features.pkl")
print("📌 Features expected by the model:")
for feat in features:
    print("-", feat)
