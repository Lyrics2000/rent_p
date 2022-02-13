

import io
import json
import os
import time
from datetime import datetime
from io import BytesIO

import stripe
from account.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.base import ContentFile, File
from django.core.mail import EmailMessage
from django.http import FileResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from homepage.models import BookingRequest, Room
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from payment.common.MpesaPaymentThread import PayViaMpesaThred
from payment.models import MpesaQuery, MpesaResquest

from .models import MpesaPayment
from .utils import validate_not_mobile

#Email imports

#####################
# Create your views here.



#mpesa callback




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
        current_site = get_current_site(request)

        site_url = f"https://{current_site}/payments/confirmation_url/"
        print("......................call_back url.................................")
        print(site_url)

        PayViaMpesaThred(data['mpesa_payment'],obj.id,1,room.id,user.id,data['emai_address'],site_url).start()

        return Response({"success":"ok"},status=status.HTTP_200_OK)


class PayWithStripe(APIView):
    def post(self,request):
        return Response({"success":"ok"})


@csrf_exempt
def confirmation_url(request):

    print(".................calling_callback.......................")
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    print(mpesa_payment)
    # payment = MpesaPayment(
    #     first_name=mpesa_payment['FirstName'],
    #     last_name=mpesa_payment['LastName'],
    #     middle_name=mpesa_payment['MiddleName'],
    #     description=mpesa_payment['TransID'],
    #     phone_number=mpesa_payment['MSISDN'],
    #     amount=mpesa_payment['TransAmount'],
    #     reference=mpesa_payment['BillRefNumber'],
    #     organization_balance=mpesa_payment['OrgAccountBalance'],
    #     type=mpesa_payment['TransactionType'],
    # )
    # payment.save()
    return render(request,'sending_success_payment.html')

    



   
    



