from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import (
    Building,
    Room,
    RoomMorePic,
    Booking,
    Payment,
    BuildingMorePic,
    SlidingImages
)
# Register your models here.

class BuildingAdmin(LeafletGeoAdmin):
    list_display = ['__str__','agent','no_of_floors','no_of_Room','location_name','geom','parking_space','security','tv_connection','account_number','owner','payment_deadline','penalties','building_main_pic','approved']
    class Meta:
        model = Building


admin.site.register(Building,BuildingAdmin)
admin.site.register(Room)
admin.site.register(RoomMorePic)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(BuildingMorePic)
admin.site.register(SlidingImages)
