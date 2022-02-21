from django.db.models import fields
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import (
    Room,
    Building,
    SavedRooms
)

class BuildingSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Building
        geo_field = "geom"
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        depth = 1
        fields = '__all__'

class SavedRoomSerializers(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    class Meta:
        model = SavedRooms
        fields = ['id','user','liked','room']



