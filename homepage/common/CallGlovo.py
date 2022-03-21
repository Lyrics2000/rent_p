import requests

class CallGlovo:
    def __init__(self,name):
        self.name = name

    def request_data(self):
       
        url = f"https://api.glovoapp.com/v3/addresslookup/pub/address?address={self.name}"

        payload={}
        headers = {
        'authority': 'api.glovoapp.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'glovo-app-version': '7',
        'glovo-app-platform': 'web',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
        'glovo-app-development-state': 'Production',
        'glovo-app-type': 'customer',
        'x-datadog-parent-id': '876210436988284347',
        'x-datadog-sampled': '1',
        'sec-ch-ua-platform': '"Linux"',
        'glovo-api-version': '14',
        'sec-ch-ua-mobile': '?0',
        'x-datadog-origin': 'rum',
        'glovo-device-id': '929902043',
        'glovo-language-code': 'en',
        'x-datadog-sampling-priority': '1',
        'accept': 'application/json',
        'x-datadog-trace-id': '3285115495462317550',
        'dnt': '1',
        'origin': 'https://glovoapp.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-language': 'en-US,en;q=0.9'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        return response.json()




# app =  CallGlovo("waruku")

# print(app.request_data())
