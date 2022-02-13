import json
from django.core.mail import EmailMessage
import threading
import time

from django.shortcuts import redirect
from account.models import User
from homepage.common.SendEmailThread import SendEmailThread
from homepage.common.sendsms import sendSms
from homepage.models import BookingRequest, Room
from payment.models import MpesaQuery, MpesaResquest
from payment.mpesa.services import PaymentService
from payment.mpesa.mpesa_credentials import MpesaC2bCredential
from payment.utils import validate_not_mobile

class PayViaMpesaThred(threading.Thread):
    def __init__(self,phone_number,request_id,amount,room_id,user_id,to_email,site_url):
        self.phone_number = phone_number
        self.request_id =  request_id
        self.amount = amount
        self.room_id = room_id
        self.user_id =  user_id
        self.to_email = to_email
        self.site_url = site_url
        threading.Thread.__init__(self)


    def mpesa_queyr(self,checkout_id,merchant_id,phone_no):
        if((checkout_id is not None) and ( merchant_id is not None) and (phone_no is not None)):
            lipa_na_mpesa = PaymentService(MpesaC2bCredential.trial_consumer_key,MpesaC2bCredential.trial_consumer_secret,MpesaC2bCredential.trial_business_shortcode,MpesaC2bCredential.passkey,live=False,debug=True)
            time.sleep(40)
            mpesa_request = lipa_na_mpesa.query_request(checkout_id)
            print(mpesa_request,"mpesa request")
            if mpesa_request["status"] == "Success":
                print("running next")
                mpesa_rs = MpesaResquest.objects.get(merchantRequestid = merchant_id, chechoutrequestid = checkout_id )
                objf,created = MpesaQuery.objects.get_or_create(mpesa_request_id = mpesa_rs )
                objf.response_code = mpesa_request['response']['ResponseCode']
                print("1")
                objf.response_description = mpesa_request['response']['ResponseDescription']
                objf.merchant_id = mpesa_request['response']['MerchantRequestID']
                print("2")
                objf.checkout_request_id = mpesa_request['response']['CheckoutRequestID']
                print("3")
                objf.result_code = mpesa_request['response']['ResultCode']
                print("4")
                objf.result_description = mpesa_request['response']['ResultDesc']
                print("5")
                objf.status =  mpesa_request['status']
                print("6")
                objf.request_id =  mpesa_request['request_id']
                objf.save()

                room = Room.objects.get(id = self.room_id)
                room.paid = True
                room.save()

                booking_obj =  BookingRequest.objects.get(id = int(self.request_id))

                
                booking_obj.paid =  True
                booking_obj.save()
                room = Room.objects.get(id = int(self.room_id))

                message = f"Successfully paid for room {room.room_name}"


                sendSms(self.phone_number,message).send_sms()
                SendEmailThread(self.to_email,message,f"Booking for {room.room_name}").start()
                redirect("payment:sending_to_mpesa")

                
                
    def startmpesaRequest(self):
        print("...........beginning mpesa request..................")
        user_obj =  User.objects.get(id= int(self.user_id))
        room = Room.objects.get(id = int(self.room_id))
        callbackurl = self.site_url
        lipa_na_mpesa = PaymentService(MpesaC2bCredential.trial_consumer_key,MpesaC2bCredential.trial_consumer_secret,MpesaC2bCredential.trial_business_shortcode,MpesaC2bCredential.passkey,live=False,debug=True) 
        app =  lipa_na_mpesa.process_request(phone_number=validate_not_mobile(str(self.phone_number)),amount=self.amount,callback_url=callbackurl,reference=f"Payment for {room.room_name}",description=f"Payment for {room.room_name}")
        print(app)
        r = json.dumps(app)
        js = json.loads(r)
        if js["status"] == "Started":
            if int(js["response"]['ResponseCode']) == 0:
                obj = MpesaResquest.objects.create(
                user_id = user_obj,
                room_id= room,
                merchantRequestid = js["response"]['MerchantRequestID'],
                chechoutrequestid = js["response"]['CheckoutRequestID'] ,
                responsecode = js["response"]['ResponseCode'] ,
                responsedescription =  js["response"]['ResponseDescription'],
                customerMessage = js["response"]['CustomerMessage'],
                status = js["status"],
                request_id = js["request_id"],
                callback_url = callbackurl)

                self.mpesa_queyr(js["response"]['CheckoutRequestID'],js["response"]['MerchantRequestID'],self.phone_number)
            
                
             

    def lipa_na_mpesa_online(self):
        lipa_na_mpesa = PaymentService(MpesaC2bCredential.trial_consumer_key,MpesaC2bCredential.trial_consumer_secret,MpesaC2bCredential.trial_business_shortcode,MpesaC2bCredential.passkey,live=False,debug=True)
        access_token = lipa_na_mpesa.get_access_token()
        if len(access_token):
            self.startmpesaRequest()
        
        return access_token
    

    def run(self):
        self.lipa_na_mpesa_online()
        
