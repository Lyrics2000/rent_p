

from django.urls import path,include
from .views import (index,signup,activate_account,logout_user,
password_reset,
reset,
change_user)

app_name = "account"

urlpatterns = [
    path('', index,name="sign_in"),
    path('signup/', signup,name="sign_up"),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate_account, name='activate'),
    path("logout_user/",logout_user,name="logout"),
    path("forgot_password/",password_reset,name="forgot_password"),
    path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        reset, name='reset'),
        path("change_user_password/",change_user,name="change_user"),
    
]



