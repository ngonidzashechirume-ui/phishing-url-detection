import pandas as pd

df = pd.read_csv("RandForest_BatchPredictions.csv")

# If the column is actually 'prediction' not 'label'
phishing_urls = df[df["prediction"] == 1]

# Show the first phishing URL
if not phishing_urls.empty:
    print("🎯 Sample Phishing URL:", phishing_urls.iloc[0]["URL"])
else:
    print("✅ No phishing URLs found in the dataset.")
