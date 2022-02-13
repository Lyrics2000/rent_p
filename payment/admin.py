from django.contrib import admin
from .models import MpesaResquest,MpesaQuery,MpesaPayment



class MpesaLipaAdmin(admin.ModelAdmin):
    list_display = ['__str__' , 'user_id','room_id','chechoutrequestid','responsecode','responsedescription']
    class Meta:
        model = MpesaResquest



admin.site.register(MpesaResquest,MpesaLipaAdmin)


class MpesaQueryAdmin(admin.ModelAdmin):
    list_display = ['__str__' ,'mpesa_request_id', 'response_code','response_description','merchant_id','checkout_request_id','result_code','result_description','status','request_id']
    class Meta:
        model = MpesaQuery

admin.site.register(MpesaQuery,MpesaQueryAdmin)
admin.site.register(MpesaPayment)


