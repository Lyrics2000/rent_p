import json
from django.core.mail import EmailMessage
import threading
import time
import requests

from django.shortcuts import redirect
from account.models import User
from homepage.common.SendEmailThread import SendEmailThread
from homepage.common.sendsms import sendSms
from homepage.models import BookingRequest, Room
from payment.models import MpesaQuery, MpesaResquest
from payment.mpesa.services import PaymentService
from payment.mpesa.mpesa_credentials import MpesaC2bCredential
from payment.utils import validate_not_mobile
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer =  get_channel_layer()

class PayViaMpesaThredC2B(threading.Thread):
    def __init__(self,phone_number,request_id,amount,room_id,user_id,to_email,site_url):
        self.phone_number = phone_number
        self.request_id =  request_id
        self.amount = amount
        self.room_id = room_id
        self.user_id =  user_id
        self.to_email = to_email
        self.site_url = site_url
        threading.Thread.__init__(self)


       
    def pay_offline(self):
        user_obj =  User.objects.get(id= int(self.user_id))
        room = Room.objects.get(id = int(self.room_id))
        
        lipa_na_mpesa = PaymentService(MpesaC2bCredential.trial_consumer_key,MpesaC2bCredential.trial_consumer_secret,MpesaC2bCredential.trial_business_shortcode,MpesaC2bCredential.passkey,live=False,debug=True) 
        app = lipa_na_mpesa.simulate_transaction(self.amount,self.phone_number,f"Payment for {room.room_name}","600995")
        print(app)


        room = Room.objects.get(id = self.room_id)
        room.paid = True
        room.save()


        message = f"Successfully paid for room {room.room_name}"


        # sendSms(self.phone_number,message).send_sms()
        # SendEmailThread(self.to_email,message,f"Booking for {room.room_name}").start()

        dicti = {
            "title":"Payment Received!!",
            "message" : "Thanks for booking a room with us"
        }

        print(dicti)

        mm =  json.loads(json.dumps(dicti))
        # to do : add later for demonstration
        time.sleep(15)
        async_to_sync(channel_layer.group_send)('mpesa_successful',{'type':'send_mpesa_success','text':mm})






    def lipa_na_mpesa_online(self):
        lipa_na_mpesa = PaymentService(MpesaC2bCredential.trial_consumer_key,MpesaC2bCredential.trial_consumer_secret,MpesaC2bCredential.trial_business_shortcode,MpesaC2bCredential.passkey,live=False,debug=True)
        access_token = lipa_na_mpesa.get_access_token()
        if len(access_token):
            self.pay_offline()
        
        return access_token
    

    def run(self):
        self.lipa_na_mpesa_online()
        
