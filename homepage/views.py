from django.forms.models import model_to_dict
from django.shortcuts import redirect, render
from django.http import JsonResponse
import json
from django.http import HttpResponse
from django.core import serializers
from .serializers import RoomSerializer,BuildingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .LOc import LocationQuery
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from account.models import (
    Agent
)
from .models import (Building, BuildingMorePic, Room,
SlidingImages,
RoomMorePic,

)

# Create your views here.
def index(request):
    all_room =  Room.objects.filter(approved = True)
    all_sliding =  SlidingImages.objects.first()
    all_room_pic =  RoomMorePic.objects.all()
    all_room_pic_count =  RoomMorePic.objects.count()
    # get current ip
    
    context = {
        'rooms' :  all_room,
        'sliding' :  all_sliding,
        'all_room_pic_count' : all_room_pic_count,
        'all_room_pic' : all_room_pic
        
    }
    return render(request,'index.html',context)


def map_search_view(request):
    if request.is_ajax and request.method == "POST":
        location =  request.POST.get("location_search")
        if len(location) > 0:
            app = LocationQuery(location.replace(" ","%20"))
            dataa =  app.resp()
            results =  dataa['results'][0]['formatted']
            latitude = dataa['results'][0]['geometry']['lat']
            longitude =  dataa['results'][0]['geometry']['lng']
            radius =  100
            point = Point(longitude,latitude)
            buildings =  Building.objects.filter(geom__distance_lt=(point, Distance(km=radius)))
            context= {
                'building':buildings,
                'formatted' : results
            }
            
            return render(request,'map.html',context)


    buildings =  Building.objects.all()
    all_rooms =  Room.objects.all()

    context= {
        'building':buildings,
        'rooms' :  all_rooms
    }
    
    return render(request,'fullmap.html',context)


class GetBUildingAPIVIEW(APIView):
    def get(self, request):
        buidlings = Building.objects.all()
        print(buidlings)
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = BuildingSerializer(buidlings,many = True)
        return Response(serializer.data)

class GetRoom(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)


def map_detailed_page(request,id):
    buildingv = Building.objects.get(id=id)
    all_rooms =  Room.objects.filter(building = buildingv )
    more_building_pic =  BuildingMorePic.objects.filter(building_id = buildingv)
    
    context = {
        'building':buildingv,
        'rooms' :all_rooms,
        'building_more_pic' :  more_building_pic
    }
    return render(request,'map_detailed.html',context)