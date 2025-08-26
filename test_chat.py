import requests

url = "http://127.0.0.1:5000/chat"
data = {"message": "Xin chào ThamAI"}

response = requests.post(url, json=data)

print("Status code:", response.status_code)
print("Response:", response.text)
