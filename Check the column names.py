import pandas as pd

df = pd.read_csv("RandForest_BatchPredictions.csv")
print("📋 Columns in CSV:", list(df.columns))
print("🔍 First few rows:\n", df.head())
