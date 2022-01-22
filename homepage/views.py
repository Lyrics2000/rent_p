import json

from account.models import Agent
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.core import serializers
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework.views import APIView

from .LOc import LocationQuery
from .models import Building, BuildingMorePic, Room, RoomMorePic, SlidingImages
from .serializers import BuildingSerializer, RoomSerializer


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
            all_rooms =  Room.objects.all()
            context= {
                'building':buildings,
                'formatted' : results,
                'all_rooms'  : all_rooms
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



class FilterRoom(APIView):
    def post(self, request):

        max_price =  request.data['max'] 
        min_price =  request.data['min']
        beds =  request.data['beds']
        print("min price :",min_price)
        print("max price :",max_price)
        print("beds : ",beds)
        if min_price != "Minimum Price" and max_price != "Maximum Price":
            print("running 1")
            all_roo =  Room.objects.filter(rent__range = [float(min_price),float(max_price)],room_type = beds)
            serializer = RoomSerializer(all_roo, many=True)
            return Response(serializer.data)

        elif min_price == "Minimum Price" and max_price != "Maximum Price":
            print("running 2")
            all_roo =  Room.objects.filter(rent__lte = float(max_price) ,room_type = beds)
            serializer = RoomSerializer(all_roo, many=True)
            return Response(serializer.data)

        
        elif max_price == "Maximum Price" and min_price != "Minimum Price" :
            print("running 4")
            all_roo =  Room.objects.filter(rent__gte = float(min_price) ,room_type = beds)
            serializer = RoomSerializer(all_roo, many=True)
            return Response(serializer.data)

        elif max_price == "Maximum Price" and min_price == "Minimum Price":
            print("running 5")
            all_roo =  Room.objects.filter(room_type = beds)
            serializer = RoomSerializer(all_roo, many=True)
            return Response(serializer.data)





        # print("min price :",min_price)
        # print("max price :",max_price)
        # rooms = Room.objects.all()
        # # the many param informs the serializer that it will be serializing more than a single article.
        # serializer = RoomSerializer(rooms, many=True)
        # return Response(serializer.data)




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


def room_detailed_page(request,id):
    
    all_rooms =  Room.objects.get(id = id )
    other_images =  RoomMorePic.objects.filter(room_id =  all_rooms)
    all_rooms_b =  Room.objects.all()
    
    print(model_to_dict(all_rooms))
    
    context = {
       
        'rooms_data' :all_rooms,
        'other_images':other_images,
        'all_rooms':all_rooms_b

      
    }
    return render(request,'room_detailed.html',context)


def request_booking(request,room_id,agent_id,user_id):
    return render(request,'booking_request.html')




def listing_listview(request):
    all_rooms = Room.objects.all()

    context = {
        'all_rooms':all_rooms
    }
    return render(request,'listing_listview.html',context)

