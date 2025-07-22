import requests

url = "http://localhost:5000/predict"
files = {'file': open('data/user-wallet-transactions.json', 'rb')}

response = requests.post(url, files=files)
print(response.json())
