import requests
import xml.etree.ElementTree as ET


class GetLeafletDate:
    def __init__(self,quer):
        self.quer =  quer

    def get_data(self):
        try:
            rep = self.quer.replace(" ","%20")
            print(rep)
    
            url = f"https://nominatim.openstreetmap.org/search?q={rep}&format=json&countrycodes=254"

            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)

            return response.json()
        except:
            rep = self.quer.split(",")[0]
            print(rep)
    
            url = f"https://nominatim.openstreetmap.org/search?q={rep}&format=json&countrycodes=254"

            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)

            return response.json()
            
    def get_osm(self,osm):
        url = f"https://www.openstreetmap.org/api/0.6/way/{osm}/full"
        payload={}
        headers = {
            'authority': 'www.openstreetmap.org',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'dnt': '1',
            'x-csrf-token': 'Sm2RTOrPWlLPModP2c7dZ4MdLmbumBPo1EMc3_ZCfiojHTYdrS8-3V9JNbofEqPwqIaUUsDCBwOeVDODExY78Q',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
            'accept': 'application/xml, text/xml, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.openstreetmap.org/way/98663668',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': '_pk_id.1.cf09=c949fda44be20261.1648915018.; _osm_directions_engine=fossgis_osrm_bike; _osm_session=a96c6ce5e61124d2e39a13adcb2839db; _pk_ref.1.cf09=%5B%22%22%2C%22%22%2C1648921386%2C%22https%3A%2F%2Fmedium.com%2F%22%5D; _pk_ses.1.cf09=1; _osm_welcome=hide; _osm_location=37.0895|-1.0469|13|M'
            }

        response = requests.request("GET", url, headers=headers, data=payload)
        data  = []

        try:
            myroot = ET.fromstring(response.text)
            print(myroot[0].attrib)
            
        
            for x in myroot:
                if(str(x.tag) == "node"):
                    data.append(x.attrib)
        except:
            pass


        return data


    def getLeafletPolygon(self):
        rep = self.quer.replace(" ","%20")
        url = f"https://nominatim.openstreetmap.org/search.php?q={rep}&polygon_geojson=1&format=jsonv2"
        payload={}
        headers = {
        'authority': 'nominatim.openstreetmap.org',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'dnt': '1',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
        'sec-ch-ua-platform': '"Linux"',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://nominatim.openstreetmap.org/ui/search.html?q=juja',
        'accept-language': 'en-US,en;q=0.9'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        return response.json()







