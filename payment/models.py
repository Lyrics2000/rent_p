from django.db import models
from rest_framework import serializers
from account.models import User
# from mainapp.models import Booking
from homepage.models import Room

# Create your models here.
class MpesaResquest(models.Model):
    user_id =  models.ForeignKey(User,on_delete=models.CASCADE)
    room_id =  models.ForeignKey(Room,on_delete=models.CASCADE)
    merchantRequestid =  models.CharField(max_length=255)
    chechoutrequestid =  models.CharField(max_length=255)
    responsecode =  models.CharField(max_length=10)
    responsedescription =  models.TextField()
    customerMessage =  models.TextField()
    status =  models.CharField(max_length=255,blank=True,null=True)
    request_id = models.CharField(max_length=255,blank=True,null=True)
    callback_url =  models.URLField(null=True,blank=True)

    def __str__(self):
        return self.merchantRequestid
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class MpesaQuery(BaseModel):
    mpesa_request_id =  models.ForeignKey(MpesaResquest,on_delete=models.CASCADE)
    response_code =  models.CharField(max_length=255)
    response_description =  models.TextField()
    merchant_id =  models.CharField(max_length=255)
    checkout_request_id =  models.CharField(max_length=255)
    result_code = models.CharField(max_length=255)
    result_description =  models.TextField()
    status = models.CharField(max_length=255)
    request_id =  models.TextField()


    def __str__(self):
        return self.response_code



class MpesaPayment(BaseModel):
    amount = models.DecimalField(max_digits=30, decimal_places=2)
    result_description = models.TextField()
    merchant_id = models.CharField(max_length=150,blank=True,null=True)
    checkout_request_id = models.CharField(max_length=150,blank=True,null=True)
    mpesaReceiptNumber = models.CharField(max_length=150,blank=True,null=True)
    name = models.CharField(max_length=150,blank=True,null=True)
    transaction_date = models.DateTimeField(blank=True,null=True)
    phone_number = models.CharField(max_length=150,blank=True,null=True)

    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'

    def __str__(self):
        return self.merchant_id



