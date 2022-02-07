

from django.shortcuts import render,redirect
from homepage.models import BookingRequest, Room
from payment.common.MpesaPaymentThread import PayViaMpesaThred

from payment.models import  MpesaResquest,MpesaQuery
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile, File
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status



import time
from django.template.loader import render_to_string

from io import BytesIO

import os

#Email imports

import json
#####################
# Create your views here.

import json
from django.http import FileResponse
import io


from datetime import datetime
#mpesa callback

import time
from .utils import validate_not_mobile
from account.models import User

from django.contrib.sites.shortcuts import get_current_site
import stripe
from django.core.mail import EmailMessage


stripe.api_key = "sk_test_51HI1b9FXATpECfwyUyt6wwmfnXQpVKAEH2rruhHsnLkLGAdtmJCBRaztSq7JNmTJCzRCdxYXYrNwHWOSogJCB5tj00gNdKZDgd"

class LipaNaMpesa(APIView):
    def post(self,request):

        payment =  request.data['payment']
        data =json.loads(payment)
        print(data)
        user = User.objects.get(id = int(request.data['user_id']))
        room =  Room.objects.get(id = int(data['room_number']) )
        obj =  BookingRequest.objects.create(
            user = user,
            room = room,
            name = data['full_name'],
            email = data['emai_address'],
            contact_phone = data['contact_number']

        )

        PayViaMpesaThred(data['mpesa_payment'],obj.id,1,room.id,user.id,data['emai_address']).start()

        return Response({"success":"ok"},status=status.HTTP_200_OK)


class PayWithStripe(APIView):
    def post(self,request):
        return Response({"success":"ok"})





   
    



