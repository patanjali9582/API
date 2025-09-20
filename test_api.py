import requests

url = "http://127.0.0.1:8000/multiply"
data = {"a": 5, "b": 4}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response:", response.json())
