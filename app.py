import requests

url = "https://nominatim.openstreetmap.org/search?q=juja&format=json&countrycodes=254"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
