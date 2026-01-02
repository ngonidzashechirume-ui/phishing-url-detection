import joblib
import pandas as pd
from urllib.parse import urlparse

# --------------------------
# 1. Load Model and Features
# --------------------------
model = joblib.load("phishing_model_africa.pkl")
features = joblib.load("model_features.pkl")

# --------------------------
# 2. Feature Extraction Function
# --------------------------
def extract_features_from_url(url):
    parsed = urlparse(url)

    features_dict = {
        'URLLength': len(url),
        'IsHTTPS': int(parsed.scheme == 'https'),
        'TLDLength': len(parsed.netloc.split('.')[-1]),
        'NoOfSubDomain': len(parsed.netloc.split('.')) - 2,
        'NoOfDegitsInURL': sum(c.isdigit() for c in url),
        'DegitRatioInURL': sum(c.isdigit() for c in url) / len(url),
        'NoOfEqualsInURL': url.count('='),
        'NoOfQMarkInURL': url.count('?'),
        'NoOfAmpersandInURL': url.count('&'),
        'NoOfOtherSpecialCharsInURL': sum(not c.isalnum() and c not in "-._~" for c in url),
        'SpacialCharRatioInURL': sum(not c.isalnum() for c in url) / len(url),
    }

    return {feat: features_dict.get(feat, 0) for feat in features}

# --------------------------
# 3. Predict a Single URL
# --------------------------
# 🔁 Change this URL to test more
url_to_test = "https://secure-bank-reset.za/login"

# Extract features and format
input_data = extract_features_from_url(url_to_test)
X = pd.DataFrame([input_data])

# Predict
prediction = model.predict(X)[0]
print(f"🔍 URL: {url_to_test}")
print("✅ Prediction:", "Phishing (1)" if prediction == 1 else "Legitimate (0)")
