import requests

class LocationQuery:
    def __init__(self,Location) -> None:
        self.url =  f"https://api.opencagedata.com/geocode/v1/json?q={Location}%20Kenya&key=03c48dae07364cabb7f121d8c1519492&no_annotations=1&language=en"

    def resp(self):
        payload={}
        headers = {
        'authority': 'api.opencagedata.com',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'dnt': '1',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
        'sec-ch-ua-platform': '"Linux"',
        'origin': 'https://www.gps-coordinates.net',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.gps-coordinates.net/',
        'accept-language': 'en-US,en;q=0.9'
        }

        response = requests.request("GET", self.url, headers=headers, data=payload)

        return response.json()
