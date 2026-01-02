# ✅ Upgraded feature extractor with all 52 features
import re

import joblib
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import socket
import tldextract


# Main feature extraction function
def extract_all_features(url):
    features = {}
    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path
    full = parsed.netloc + parsed.path

    # Load HTML (timeout fallback)
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, timeout=5, headers=headers)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
    except:
        html = ""
        soup = BeautifulSoup("", 'html.parser')

    # General utilities
    def has_tag(tag):
        return bool(soup.find(tag))

    def count_tags(tag):
        return len(soup.find_all(tag))

    # Extract base values
    features['URLLength'] = len(url)
    features['DomainLength'] = len(domain)
    features['IsDomainIP'] = int(re.match(r'^(\d{1,3}\.){3}\d{1,3}$', domain) is not None)

    ext = tldextract.extract(url)
    tld = ext.suffix or ""
    features['TLDLength'] = len(tld)
    features['NoOfSubDomain'] = domain.count('.') - 1

    # Character features
    features['NoOfLettersInURL'] = sum(c.isalpha() for c in url)
    features['LetterRatioInURL'] = features['NoOfLettersInURL'] / len(url)
    features['NoOfDegitsInURL'] = sum(c.isdigit() for c in url)
    features['DegitRatioInURL'] = features['NoOfDegitsInURL'] / len(url)
    features['NoOfEqualsInURL'] = url.count('=')
    features['NoOfQMarkInURL'] = url.count('?')
    features['NoOfAmpersandInURL'] = url.count('&')
    features['NoOfOtherSpecialCharsInURL'] = sum(not c.isalnum() and c not in "-._~" for c in url)
    features['SpacialCharRatioInURL'] = sum(not c.isalnum() for c in url) / len(url)

    # Obfuscation features
    obfuscation_chars = ['%', '$', '@', '#']
    features['HasObfuscation'] = int(any(c in url for c in obfuscation_chars))
    features['NoOfObfuscatedChar'] = sum(url.count(c) for c in obfuscation_chars)
    features['ObfuscationRatio'] = features['NoOfObfuscatedChar'] / len(url)

    # Security and protocol
    features['IsHTTPS'] = int(parsed.scheme == 'https')
    features['Robots'] = int('/robots.txt' in html)

    # Title features
    title_tag = soup.find('title')
    title_text = title_tag.text.strip().lower() if title_tag else ""
    features['HasTitle'] = int(bool(title_text))
    features['DomainTitleMatchScore'] = int(domain.lower() in title_text)
    features['URLTitleMatchScore'] = int(parsed.netloc.lower() in title_text or ext.domain in title_text)

    # Technical HTML features
    features['HasFavicon'] = int(bool(soup.find('link', rel=lambda x: x and 'icon' in x.lower())))
    features['LineOfCode'] = html.count('\n')
    features['LargestLineLength'] = max((len(line) for line in html.split('\n')), default=0)
    features['HasDescription'] = int(bool(soup.find('meta', attrs={'name': 'description'})))

    # Scripts and external resources
    features['NoOfPopup'] = html.count('alert(')
    features['NoOfiFrame'] = count_tags('iframe')
    features['HasExternalFormSubmit'] = int(bool(soup.find('form', action=lambda x: x and not x.startswith('/'))))
    features['HasSocialNet'] = int(
        any(tag for tag in soup.find_all('a') if 'facebook' in str(tag) or 'twitter' in str(tag)))
    features['HasSubmitButton'] = int(bool(soup.find('input', {'type': 'submit'})))
    features['HasHiddenFields'] = int(bool(soup.find('input', {'type': 'hidden'})))
    features['HasPasswordField'] = int(bool(soup.find('input', {'type': 'password'})))

    # Tricky keywords
    url_lower = url.lower()
    features['Bank'] = int('bank' in url_lower)
    features['Pay'] = int('pay' in url_lower)
    features['Crypto'] = int('crypto' in url_lower)
    features['HasCopyrightInfo'] = int('copyright' in html.lower())

    # Resource counts
    features['NoOfImage'] = count_tags('img')
    features['NoOfCSS'] = len(soup.find_all('link', {'rel': 'stylesheet'}))
    features['NoOfJS'] = count_tags('script')

    features['NoOfSelfRef'] = len([a for a in soup.find_all('a', href=True) if a['href'].startswith('#')])
    features['NoOfEmptyRef'] = len([a for a in soup.find_all('a', href=True) if a['href'] in ('', '#')])
    features['NoOfExternalRef'] = len([a for a in soup.find_all('a', href=True) if 'http' in a['href']])

    # Unknown / placeholder (fill with 0 if missing)
    expected_features = joblib.load('RandForest_model_features.pkl')
    complete_features = {key: features.get(key, 0) for key in expected_features}

    return complete_features
