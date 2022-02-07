from os import name
from django.urls import path

from .views import (


    LipaNaMpesa,



    qr_code,
    generate_pdf
)

app_name = "payment"
urlpatterns = [
    path('lipa_na_mpesa/',LipaNaMpesa.as_view(),name="lipa_online_mpesa"),
   
  
    path('qr_code/',qr_code,name="qr_code"),
    path('generate_pdf/',generate_pdf,name="generate_pdf")

]

