import requests
import xml.etree.ElementTree as ET


url = "https://nominatim.openstreetmap.org/reverse?lat=-1.5176837&lon=37.2634146"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)


# print(response.text)



myroot = ET.fromstring(response.text)
print(myroot[0].attrib)
data  = []
for x in myroot:
  if(str(x.tag) == "node"):
    data.append(x.attrib)


print(data)

