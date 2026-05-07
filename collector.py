import requests

url = "https://www.jobbank.gc.ca/home"

response = requests.get(url)

print("Status Code:", response.status_code)
print(response.text[:500])