from os import name
from django.urls import path

from .views import (


    LipaNaMpesa,

)

app_name = "payment"
urlpatterns = [
    path('lipa_na_mpesa/',LipaNaMpesa.as_view(),name="lipa_online_mpesa"),
   
  
 

]

