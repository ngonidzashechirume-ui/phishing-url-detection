import pandas as pd

# Load your CSV predictions
df = pd.read_csv("RandForest_BatchPredictions.csv")

# Merge with original dataset that contains the URLs
original_df = pd.read_csv("PhiUSIIL_Phishing_URL_Dataset.csv")

# Find rows where the model predicted phishing and it is actually phishing
phishing_df = df[(df["Prediction"] == 1) & (df["Actual Label"] == 1)]

# Reset index to align if necessary
phishing_df = phishing_df.reset_index(drop=True)
original_df = original_df.reset_index(drop=True)

# Get corresponding URLs from original dataset using index
sample_urls = original_df.loc[phishing_df.index, "URL"]

# Show the first 5 phishing URLs for testing
print("🚨 Sample Phishing URLs to test in extension:")
for url in sample_urls.head(5):
    print("🔗", url)
