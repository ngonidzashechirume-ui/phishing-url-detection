from urllib.parse import urlparse

def extract_features_from_url(url):
    parsed = urlparse(url)

    features = {
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

    return features
