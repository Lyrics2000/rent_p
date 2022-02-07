

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
from django.core.mail import EmailMessage


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


@login_required(login_url="account:sign_in")
def qr_code(request):
    user =  request.user
    booking =  request.session.get('booking_id')
    booking_obj =  Booking.objects.get(id = booking)
    bkn = {}
    bkn['first_name'] =  request.user.first_name
    bkn['last_name'] =  request.user.last_name
    bkn['phone'] =  request.user.phone
    bkn['fare_amount'] = booking_obj.fare_amount
    bkn['id'] =  booking_obj.id
    bkn['total_amount'] = booking_obj.total_amount
    bkn['number_of_seats'] = booking_obj.number_of_seats
    bkn['booking_status'] = booking_obj.booking_status

    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(str(bkn), image_factory=factory, box_size=20)
    stream = BytesIO()
    img.save(stream)
    srv = stream.getvalue().decode()
    svg2png(bytestring=srv,write_to='output.png')
    # Using File
    with open('output.png', 'rb') as fi:
        my_file = File(fi, name=os.path.basename(fi.name))
        booking_obj.qr_code = my_file
        booking_obj.save()
     
        # del request.session['phone']
        # del request.session['booking_id']
        # del  request.session['checkout_id']
        # del request.session['merchant_id']
        # del request.session['phone_no']
        
        context = {
            'svg': booking_obj
        }


    return render(request, "qrcode.html", context=context)

@login_required(login_url="account:sign_in")
def generate_pdf(request):
    booking =  request.session.get('booking_id')
    booking_obj =  Booking.objects.get(id = booking)
    bkn = {}
    bkn1 ={}
    bkn2 = {}
    bkn3 = {}
    bkn4 ={}
    bkn5 ={}
    bkn6 ={}
    bkn7 ={}
    bkn['first_name'] =  request.user.first_name
    bkn1['last_name'] =  request.user.last_name
    bkn2['phone'] =  request.user.phone
    bkn3['fare_amount'] = booking_obj.fare_amount
    bkn4['id'] =  booking_obj.id
    bkn5['total_amount'] = booking_obj.total_amount
    bkn6['number_of_seats'] = booking_obj.number_of_seats
    bkn7['booking_status'] = booking_obj.booking_status

    # generae byte stream
    buf  =  io.BytesIO()
    # create canvas
    c =  canvas.Canvas(buf,pagesize=letter,bottomup=1)
    # creat a text object
    textob =  c.beginText()
 
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",14)

    # add text
    textob.textLine(str(bkn))
    textob.textLine(str(bkn1))
    textob.textLine(str(bkn2))
    textob.textLine(str(bkn3))
    textob.textLine(str(bkn4))
    textob.textLine(str(bkn5))
    textob.textLine(str(bkn6))
    textob.textLine(str(bkn7))
    with open('output.png', 'rb') as fi:
       
        c.drawImage(os.path.basename(fi.name),inch, inch, mask='auto')
        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)
        del request.session['phone']
        del request.session['booking_id']
        del  request.session['checkout_id']
        del request.session['merchant_id']
        del request.session['phone_no']
        return FileResponse(buf,as_attachment=True,filename='receipt.pdf')
        


   
    



