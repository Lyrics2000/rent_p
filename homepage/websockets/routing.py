from django.urls import path
from .consumer import (
PaymentSuccessfullMessage)


ws_urlpattern = [
    path('ws/payment_successfull/',PaymentSuccessfullMessage.as_asgi())   
]

