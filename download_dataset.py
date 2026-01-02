import pandas as pd

# Replace 'phiusiil_dataset.csv' with your actual filename
df = pd.read_csv('PhiUSIIL_Phishing_URL_Dataset.csv')

# Show the shape and first few rows
print(df.shape)
print(df.head())
print(df.columns)
