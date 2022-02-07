import requests
import json
from requests import api
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64


class MpesaC2bCredential:
    trial_consumer_key = "tyvsDnVyL3rI4VfMDPJxKWR80y7jvSEt"
    trial_consumer_secret = "7UXHgE4i0G8kPhg9"
    trial_business_shortcode = "174379"

    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    CallBackURL = "https://shrouded-reef-57090.herokuapp.com/payment/c2b/confirmation/"


class MpesaAccessToken:

    def __init__(self,api_URL,consumer_key,consumer_secret):
        self.api_URL =  api_URL
        self.consumer_key =  consumer_key
        self.consumer_secret = consumer_secret

    def get_access_token(self):

        r = requests.get(self.api_URL,auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret))
        mpesa_access_token = json.loads(r.text)
        return mpesa_access_token['access_token']


class LipanaMpesaPpassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = "174379"
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    Business_short_code = "174379"
    Test_c2b_shortcode = "600344"
    data_to_encode = Business_short_code + passkey + lipa_time

    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')


class MpesaSTKPUsh:
    def __init__(self,live=False,consumer_key="",consumer_secret=""):
        self.test_server = "https://sandbox.safaricom.co.ke"
        self.live_server = "https://api.safaricom.co.ke"
        self.process_request_path = '/mpesa/stkpush/v1/processrequest'
        self.query_request_path = '/mpesa/stkpushquery/v1/query'
        self.access_token_path = '/oauth/v1/generate?grant_type=client_credentials'
        self.test_shortcode = 174379
        self.live =  live
        self.test_passkey = "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjExMTA5MDEwMTEw"
        self.consumer_key =  consumer_key
        self.consumer_secret =  consumer_secret

    def get_access_token(self):
        if(self.live):
            url = self.live_server + self.access_token_path
            response = requests.get(url, auth=(self.consumer_key, self.consumer_secret))
            if response.status_code == 200:
                data = response.json()
                self.access_token = data['access_token']
                return self.access_token
            else:
                return None
        else:
            url = self.test_server + self.access_token_path
            response = requests.get(url, auth=(self.consumer_key, self.consumer_secret))
            if response.status_code == 200:
                data = response.json()
                self.access_token = data['access_token']
                return self.access_token
            else:
                return None



    def send_stk_push(self,live_business_code,live_password,phone_number,amount,callback_url,company_reference,transaction_description):
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + str(self.get_access_token())
                }
            if(self.live):
                url_live = self.live_server + self.process_request_path
                payload = {
                    "BusinessShortCode": live_business_code,
                    "Password": str(live_password),
                    "Timestamp": timestamp,
                    "TransactionType": "CustomerPayBillOnline",
                    "Amount": amount,
                    "PartyA": phone_number,
                    "PartyB": live_business_code,
                    "PhoneNumber": phone_number,
                    "CallBackURL": str(callback_url),
                    "AccountReference": company_reference,
                    "TransactionDesc": transaction_description
                }
                response = requests.request("POST", url_live, headers = headers, data = payload)
                if response.status_code == 200:
                    return response.text.encode('utf8')
                else:
                    return None

            else:
                print("ak")
                url_dummy = self.test_server + self.process_request_path
                payload2 = {
                    "BusinessShortCode": self.test_shortcode,
                    "Password": str(self.test_passkey),
                    "Timestamp": timestamp,
                    "TransactionType": "CustomerPayBillOnline",
                    "Amount": amount,
                    "PartyA": phone_number,
                    "PartyB": self.test_shortcode,
                    "PhoneNumber": phone_number,
                    "CallBackURL": str(callback_url),
                    "AccountReference": company_reference,
                    "TransactionDesc": transaction_description
                }
                responsec = requests.request("POST", url_dummy, headers = headers, data = payload2)
                return responsec.text.encode('utf8')
                # if response.status_code == 200:
                #     return response.text.encode('utf8')
                # else:
                #     return None



            

    



    
