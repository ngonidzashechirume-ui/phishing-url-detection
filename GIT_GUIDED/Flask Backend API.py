from flask import Flask, request, jsonify
import joblib
import pandas as pd
from urllib.parse import urlparse
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# Load trained model and feature list
model = joblib.load('Random_Forest TRAINED_MODEL.pkl')
features = joblib.load('RandForest_model_features.pkl')

# Enhanced feature extraction matching all 52 features
def extract_full_features(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path

    # Try to fetch HTML content
    try:
        response = requests.get(url, timeout=5)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
    except:
        soup = BeautifulSoup("", 'html.parser')
        html = ""

    def get_title():
        title_tag = soup.title
        return title_tag.text.strip() if title_tag else ""

    def match_score(a, b):
        return len(set(a.lower().split()) & set(b.lower().split())) / max(len(set(a.lower().split()) | set(b.lower().split())), 1) * 100

    title = get_title()

    features_dict = {
        'URLLength': len(url),
        'DomainLength': len(domain),
        'IsDomainIP': int(re.fullmatch(r"\d+\.\d+\.\d+\.\d+", domain) is not None),
        'URLSimilarityIndex': 100,
        'CharContinuationRate': 1 if ".." not in url else 0,
        'TLDLegitimateProb': 0.5,
        'URLCharProb': sum(c.isalnum() for c in url) / len(url),
        'TLDLength': len(domain.split('.')[-1]),
        'NoOfSubDomain': len(domain.split('.')) - 2,
        'HasObfuscation': 0,
        'NoOfObfuscatedChar': 0,
        'ObfuscationRatio': 0.0,
        'NoOfLettersInURL': sum(c.isalpha() for c in url),
        'LetterRatioInURL': sum(c.isalpha() for c in url) / len(url),
        'NoOfDegitsInURL': sum(c.isdigit() for c in url),
        'DegitRatioInURL': sum(c.isdigit() for c in url) / len(url),
        'NoOfEqualsInURL': url.count('='),
        'NoOfQMarkInURL': url.count('?'),
        'NoOfAmpersandInURL': url.count('&'),
        'NoOfOtherSpecialCharsInURL': sum(not c.isalnum() and c not in "-._~" for c in url),
        'SpacialCharRatioInURL': sum(not c.isalnum() for c in url) / len(url),
        'IsHTTPS': int(parsed.scheme == 'https'),
        'LineOfCode': len(html.splitlines()),
        'LargestLineLength': max([len(line) for line in html.splitlines()] or [0]),
        'HasTitle': int(bool(title)),
        'DomainTitleMatchScore': match_score(domain, title),
        'URLTitleMatchScore': match_score(url, title),
        'HasFavicon': int(bool(soup.find("link", rel="icon"))),
        'Robots': 0,
        'IsResponsive': 1,
        'NoOfURLRedirect': 0,
        'NoOfSelfRedirect': 0,
        'HasDescription': int(bool(soup.find("meta", attrs={'name': 'description'}))),
        'NoOfPopup': len(soup.find_all("script", string=re.compile(r"window\.open"))),
        'NoOfiFrame': len(soup.find_all("iframe")),
        'HasExternalFormSubmit': int(any("http" in form.get("action", '') for form in soup.find_all("form"))),
        'HasSocialNet': int(any(net in html for net in ["facebook.com", "twitter.com", "linkedin.com"])),
        'HasSubmitButton': int(bool(soup.find("button", {"type": "submit"}) or soup.find("input", {"type": "submit"}))),
        'HasHiddenFields': int(bool(soup.find("input", {"type": "hidden"}))),
        'HasPasswordField': int(bool(soup.find("input", {"type": "password"}))),
        'Bank': int("bank" in html.lower()),
        'Pay': int("pay" in html.lower()),
        'Crypto': int("crypto" in html.lower()),
        'HasCopyrightInfo': int("©" in html or "copyright" in html.lower()),
        'NoOfImage': len(soup.find_all("img")),
        'NoOfCSS': len(soup.find_all("link", rel="stylesheet")),
        'NoOfJS': len(soup.find_all("script")),
        'NoOfSelfRef': html.count(domain),
        'NoOfEmptyRef': html.count("\"\""),
        'NoOfExternalRef': html.count("http")
    }

    return {feat: features_dict.get(feat, 0) for feat in features}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_address = request.remote_addr

    print(f"\n⏰ [{timestamp}] 🌐 Request from {ip_address}")
    print(f"🔍 URL: {url}")

    features_dict = extract_full_features(url)
    print(f"📊 Extracted Features: {features_dict}")

    X = pd.DataFrame([features_dict])
    raw_prediction = model.predict(X)[0]
    prediction = 1 - int(raw_prediction)

    print(f"✅ Prediction: {prediction} (1 = phishing, 0 = safe)")

    with open("ml_predictions_log.txt", "a") as f:
        f.write(f"[{timestamp}] {ip_address} - {url} => Prediction: {prediction}\n")

    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    from waitress import serve
    print("🚀 Starting production server with Waitress on http://127.0.0.1:5000")
    serve(app, host='127.0.0.1', port=5000)
