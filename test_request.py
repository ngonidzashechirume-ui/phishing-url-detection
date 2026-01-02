import requests

response = requests.post(
    "http://127.0.0.1:5000/predict",
    json={"url": "https://secure-bank-reset.za/login"}
)

print(response.json())