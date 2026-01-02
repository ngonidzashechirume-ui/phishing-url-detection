import pandas as pd

# Load the full original dataset
df = pd.read_csv("PhiUSIIL_Phishing_URL_Dataset.csv")

# Filter only African ccTLDs
african_ccTLDs = ['.za', '.ng', '.ke', '.gh', '.tz', '.ug', '.bw', '.zm', '.zw', '.sn', '.cm', '.dz', '.ma', '.eg']
df_africa = df[df['URL'].str.contains('|'.join(african_ccTLDs), na=False)]

# Filter phishing URLs only
phishing_urls = df_africa[df_africa["label"] == 1]

# Pick one sample
sample_url = phishing_urls["URL"].iloc[0]
print("🚨 Sample phishing URL for test:", sample_url)
