from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

# Register your models here.
from .models import User,Agent


admin.site.register(User)
admin.site.register(Agent,LeafletGeoAdmin)
