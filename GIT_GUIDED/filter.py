import pandas as pd

# Load the dataset
df = pd.read_csv('PhiUSIIL_Phishing_URL_Dataset.csv')  # adjust filename if needed

# List of African ccTLDs
african_ccTLDs = ['.ng', '.za', '.ke', '.gh', '.ug', '.tz', '.eg', '.sn', '.rw', '.dz']

# Filter URLs containing African domain extensions
african_urls = df[df['URL'].str.contains('|'.join(african_ccTLDs), na=False)]

# Show results
print(african_urls.shape)
print(african_urls[['URL', 'label']].head())
