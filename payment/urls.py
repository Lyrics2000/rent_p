from os import name
from django.urls import path

from .views import (


    LipaNaMpesa,
    confirmation_url

)

app_name = "payment"
urlpatterns = [
    path('lipa_na_mpesa/',LipaNaMpesa.as_view(),name="lipa_online_mpesa"),
    path("confirmation_url/",confirmation_url,name="sending_to_mpesa")
   
  
 

]

