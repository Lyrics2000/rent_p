from os import name
from django.urls import path

from .views import (


    LipaNaMpesa,
    confirmation_url,
    customer_to_business,
    LipaNaMpesaC2B

)

app_name = "payment"
urlpatterns = [
    path('lipa_na_mpesa/',LipaNaMpesa.as_view(),name="lipa_online_mpesa"),
    path("confirmation_url/",confirmation_url,name="sending_to_mpesa"),
    path("customer_to_business/",customer_to_business,name="customer_to_business"),
    path("pay_c2b/",LipaNaMpesaC2B.as_view(),name="c2b_p")
   
  
 

]

