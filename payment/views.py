

import io
import json
import os
import time
from datetime import datetime
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
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
        print(site_url)

        PayViaMpesaThred(data['mpesa_payment'],obj.id,1,room.id,user.id,data['emai_address'],site_url).start()

        return Response({"success":"ok"},status=status.HTTP_200_OK)


class PayWithStripe(APIView):
    def post(self,request):
        return Response({"success":"ok"})

@csrf_exempt 
def confirmation_url(request):
    if request.method == "POST":
      
        print("...............confirmation beginning...................")
        mpesa_body =request.body.decode('utf-8')
        mpesa_payment = json.loads(mpesa_body)
        body = mpesa_payment['Body']["stkCallback"]
        if body["ResultCode"] == 0:
            merchant_id = body['MerchantRequestID']
            checkout_request_id = body["CheckoutRequestID"]
            result_description = body['ResultDesc']
            callback_metadata = body['CallbackMetadata']['Item']
            amount = callback_metadata[0]['Value']
            MpesaReceiptNumber = callback_metadata[1]['Value']
            name = callback_metadata[2]['Name']
            transaction_date_year = str(callback_metadata[3]['Value'])[0:4]
            transaction_date_month = str(callback_metadata[3]['Value'])[4:6]
            transaction_date_day = str(callback_metadata[3]['Value'])[6:8]
            transaction_hours = str(callback_metadata[3]['Value'])[8:10]
            transaction_min = str(callback_metadata[3]['Value'])[10:12]
            transaction_sec = str(callback_metadata[3]['Value'])[12:14]
            day_string = transaction_date_year + "/" + transaction_date_month+ "/" + transaction_date_day + "  " + transaction_hours + ":" + transaction_min + ":" + transaction_sec + ".0"
            datetime_object = datetime.strptime(day_string, '%Y/%m/%d %H:%M:%S.%f')
            phone_number = callback_metadata[4]['Value']
            print("........saving details.................")
            payment,created = MpesaPayment.objects.get_or_create(merchant_id = merchant_id, checkout_request_id = checkout_request_id )
            payment.amount =  amount
            payment.result_description = result_description
            payment.merchant_id = merchant_id
            payment.checkout_request_id = checkout_request_id
            payment.mpesaReceiptNumber  = MpesaReceiptNumber
            payment.name = name
            payment.transaction_date  = datetime_object
            payment.phone_number  = phone_number
            payment.save()


            # payment = MpesaPayment(
            #     amount = amount,
            #     result_description= result_description,
            #     merchant_id= merchant_id,
            #     checkout_request_id=checkout_request_id,
            #     mpesaReceiptNumber= MpesaReceiptNumber,
            #     name= name,
            #     transaction_date=datetime_object,
            #     phone_number=phone_number

            # )
            # payment.save()
            print("...........saved details...................")
        print("........... redirecting ...................")
        return render(render,'sending_success_payment.html')

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }

    return JsonResponse(dict(context))



