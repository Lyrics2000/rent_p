from cgitb import html
from http.client import HTTPResponse
import json
from django.db.models import Q
from threading import Thread
from urllib import request

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from account.models import Agent, User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Min,Max

from django.http import HttpResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.core import serializers
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework.views import APIView
from homepage.common.SendEmailThread import SendEmailThread

from homepage.common.sendsms import sendSms
from homepage.sendEmailT import SendEmailKanzi

from .LOc import LocationQuery
from .models import BookingRequest, Building, BuildingMorePic, Room, RoomMorePic, SavedRooms, SlidingImages,BookTour
from .serializers import BuildingSerializer, RoomSerializer, SavedRoomSerializers

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context


# Create your views here.
def index(request):

    if request.user.is_authenticated:
            all_room =  Room.objects.filter(approved = True,paid = False)
            user_obj =  User.objects.get(id = request.user.id)
            all_sliding =  SlidingImages.objects.first()
            all_room_pic =  RoomMorePic.objects.all()
            all_room_pic_count =  RoomMorePic.objects.count()
            saved_rentals =  SavedRooms.objects.filter(user =  user_obj,liked=True)
            print(saved_rentals)
            empty_list = []
            if saved_rentals:
               
                for j in  all_room:
                    try:
                        sv = SavedRooms.objects.get(user =  user_obj,liked=True,room__id = j.id)
                       
                        dicti = {}
                        dicti['room'] = j
                        dicti['saved'] = True
                        empty_list.append(dicti)
                    except SavedRooms.DoesNotExist:
                        dicti = {}
                        dicti['room'] = j
                        dicti['saved'] = False
                        empty_list.append(dicti)



                    


                
                            
                       

            else:
                for i in  all_room:
                        dicti = {}
                        dicti['room'] = i
                        dicti['saved'] = False
                        empty_list.append(dicti)

            print(empty_list)


                    
            
            # get current ip
            
            context = {
                'rooms' :  empty_list,
                'sliding' :  all_sliding,
                'all_room_pic_count' : all_room_pic_count,
                'all_room_pic' : all_room_pic,
                'saved_rentals':saved_rentals
                
            }
            return render(request,'index.html',context)


    all_room =  Room.objects.filter(approved = True,paid = False)
    all_sliding =  SlidingImages.objects.first()
    all_room_pic =  RoomMorePic.objects.all()
    all_room_pic_count =  RoomMorePic.objects.count()
    # get current ip
    empty_list= []
    for i in  all_room:
                dicti = {}
                dicti['room'] = i
                dicti['saved'] = False
                empty_list.append(dicti)

    print(empty_list)


    
    context = {
        'rooms' :  empty_list,
        'sliding' :  all_sliding,
        'all_room_pic_count' : all_room_pic_count,
        'all_room_pic' : all_room_pic,
        'saved_rentals':None
        
    }
    return render(request,'index.html',context)


def map_search_view(request):
    if request.is_ajax and request.method == "POST":
        location =  request.POST.get("location_search")
        building =  request.POST.get('building')
    
        print("checking 1")
        
        app = LocationQuery(location.replace(" ","%20"))
        dataa =  app.resp()
        print("dataa",dataa)
        results =  dataa['results'][0]['formatted']
        latitude = dataa['results'][0]['geometry']['lat']
        longitude =  dataa['results'][0]['geometry']['lng']

        radius =  100
        point = Point(longitude,latitude)
        # buildings =  Building.objects.filter(geom__distance_lt=(point, Distance(km=radius)))
    
        buildings =  Building.objects.all()
    
        # all_rooms =  Room.objects.filter(approved = True,paid = False,building__geom__distance_lt=(point, Distance(km=radius)) )
        all_rooms =  Room.objects.filter(approved = True,paid = False)
        context= {
            'zoom_lat':latitude,
            'zoom_lng': longitude,
            'zoom_rad' : radius,
            'type': building,
            'dataa_tyoe': dataa,
            'criteria_mk' : location,
            'formatted' : f"Search for : {location}",
            'all_rooms'  : all_rooms
        }
        
        return render(request,'map_edited.html',context)
    all_rooms =  Room.objects.filter(approved = True,paid = False)

    context= {
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


    def post(self,request):
        id =  request.data['id']
        print("the id",id)
        buidlings = Building.objects.get(id = int(id))
        print("building d",buidlings)
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = BuildingSerializer(buidlings)
        return Response(serializer.data)



class GetRoomAl(APIView):
    def get(self,request):
        criteria = request.query_params
        print(criteria)
        all_roomms = Room.objects.filter(approved = True,paid = False)
        room_serializer =  RoomSerializer(all_roomms,many = True)
        return Response(room_serializer.data)


    def post(self,request):
        longitude = request.data['longitudkie']
        latitude = request.data['latitude']
        print(latitude,longitude)

        radius = 500
        
        point = Point(float(latitude),float(longitude))
        # all_rooms =  Room.objects.filter(approved = True,paid = False,building__geom__distance_lte=(point, Distance(km=radius)) )
        all_rooms =  Room.objects.filter(approved = True,paid = False)
        
        # if (typee == "building"):
            # buidling = Building.objects.filter()
            # building__building_name__in = criteria
            # all_roomms = Room.objects.filter(Q(approved = True,paid = False)) 
        #     empty_list = []
        #     for i in all_roomms:
        #         ratio = fuzz.partial_ratio(i.building.building_name.lower(),criteria.lower())
        #         if (ratio >=70):
        #             empty_list.append(i)

        #     print(empty_list)
        #     # all_roomms = Room.objects.filter(approved = True,paid = False,buiding__building_name__contains = criteria)
        #     room_serializer =  RoomSerializer(empty_list,many = True)
        #     return Response(room_serializer.data)

        # elif (typee == "location"):
        #     all_roomms = Room.objects.filter(Q(approved = True,paid = False)) 
        #     empty_list = []
        #     for i in all_roomms:
        #         ratio = fuzz.partial_ratio(i.building.location_name.lower(),criteria.lower())
        #         if (ratio >=70):
        #             empty_list.append(i)

        #     print(empty_list)
            # all_roomms = Room.objects.filter(approved = True,paid = False,buiding__building_name__contains = criteria)
        room_serializer =  RoomSerializer(all_rooms,many = True)
        return Response(room_serializer.data)






class GetRoom(APIView):
    def get(self, request):
        rooms = Room.objects.filter(approved = True,paid = False)
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
        
        print("running 1")
        all_roo =  Room.objects.filter(rent__range = [float(min_price),float(max_price)],room_type = beds,approved = True,paid = False)
        serializer = RoomSerializer(all_roo, many=True)
        return Response(serializer.data)





class FilterSavedRoom(APIView):

    def post(self, request):
        print("running post request...")
        
        max_price =  request.data['max'] 
        user_id =  request.data['id']
        min_price =  request.data['min']
        beds =  request.data['beds']
        print("min price :",min_price)
        print("max price :",max_price)
        print("beds : ",beds)
        user_obj =  User.objects.get(id =  user_id)
        print("user obj",user_obj)
        if user_obj:
        
            print("signed in 1")
            all_roo =  SavedRooms.objects.filter(user= user_obj,room__rent__range = [float(min_price),float(max_price)],room__room_type = beds,liked = True)
            serializer = SavedRoomSerializers(all_roo, many=True)
            return Response(serializer.data)
        else:
            print("not signed in 1")
            all_roo =  SavedRooms.objects.filter(user= user_obj,room__rent__range = [float(min_price),float(max_price)],room__room_type = beds,liked = True)
            serializer = SavedRoomSerializers(all_roo, many=True)
            return Response(serializer.data)


     
     





def map_detailed_page(request,id):
    buildingv = Building.objects.get(id=id)
    all_rooms =  Room.objects.filter(building = buildingv,approved = True,paid = False )
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
    all_rooms_b =  Room.objects.filter(approved = True,paid = False)
    
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

    if request.user.is_authenticated:
        user_obj =  User.objects.get(id =  request.user.id)
        all_room = Room.objects.filter(approved = True,paid = False)
        
        saved_rentals =  SavedRooms.objects.filter(user =  user_obj,liked=True)
        print(saved_rentals)
        empty_list = []
        if saved_rentals: 
            for j in  all_room:
                try:
                    sv = SavedRooms.objects.get(user =  user_obj,liked=True,room__id = j.id)
                    
                    dicti = {}
                    dicti['room'] = j
                    dicti['saved'] = True
                    empty_list.append(dicti)
                except SavedRooms.DoesNotExist:
                    dicti = {}
                    dicti['room'] = j
                    dicti['saved'] = False
                    empty_list.append(dicti)


        else:
            for i in  all_room:
                dicti = {}
                dicti['room'] = i
                dicti['saved'] = False
                empty_list.append(dicti)

        print("authenticated",empty_list)

        
        all_rooms = Room.objects.filter(approved = True,paid = False)
        min_rent = Room.objects.filter().annotate(Min('rent')).order_by('rent')[0]
        subtract = len(all_rooms) - 1
        max_rent = Room.objects.filter().annotate(Max('rent')).order_by('rent')[subtract]
        print(min_rent.rent,max_rent.rent)
        context = {
        'all_rooms':empty_list,
         'min_rent' : min_rent.rent,
        'max_rent' : max_rent.rent
        }
        return render(request,'listing_listview.html',context)



    all_rooms = Room.objects.filter(approved = True,paid = False)

    min_rent = Room.objects.filter().annotate(Min('rent')).order_by('rent')[0]
    subtract = len(all_rooms) - 1
    max_rent = Room.objects.filter().annotate(Max('rent')).order_by('rent')[subtract]
    print(min_rent.rent,max_rent.rent)
    empty_list = []
    for i in  all_rooms:
            dicti = {}
            dicti['room'] = i
            dicti['saved'] = False
            empty_list.append(dicti)

    print("not authenticated",empty_list)

    context = {
        'all_rooms':empty_list,
        'min_rent' : min_rent.rent,
        'max_rent' : max_rent.rent

    }


    return render(request,'listing_listview.html',context)



def book_request(request,id):
    
    if request.method == "POST":
        date =  request.POST.get("date")
        time =  request.POST.get("time")
        phone =  request.POST.get("phone")
        email =  request.POST.get("email")
        roo =  Room.objects.get(id =  id)
        BookTour.objects.create(room = roo,
        day = date,
        time =  time,
        phone =  phone,
        email =  email


        )
        print(phone)
        message = f"Hello,thanks for scheduling a tour with us for  room {roo.room_name},in {roo.building.location_name}, on {time} and date {date}"
        sendSms(phone,message).send_sms()
        SendEmailThread(email=email.lower(),message=message,subject="Room Booking").start()

       

        return JsonResponse({"success":"ok"})

    get_room =  Room.objects.get(id = id)
    context = {
        'room':get_room
    }
    return render(request,'book_request.html',context)

@login_required(login_url="account:sign_in")
def saved_room(request,id):
    get_r = Room.objects.get(id = id)
    user_obj =  User.objects.get(id =  request.user.id)
    print(user_obj)
    obj,created = SavedRooms.objects.get_or_create(room = get_r,user = user_obj)
    obj.liked =  True
    obj.save()
    

    all_saved_rooms = SavedRooms.objects.filter(user = user_obj,liked=True)
    print("jjj",all_saved_rooms)
    all_rooms = Room.objects.filter(approved = True,paid = False)
    min_rent = Room.objects.filter(approved = True,paid = False).annotate(Min('rent')).order_by('rent')[0]
    subtract = len(all_rooms) - 1
    max_rent = Room.objects.filter(approved = True,paid = False).annotate(Max('rent')).order_by('rent')[subtract]
    print(min_rent.rent,max_rent.rent)

    context = {
        'saved_rooms':all_saved_rooms,
        'min_rent':min_rent.rent,
        'max_rent':max_rent.rent

    }

    return render(request,'saved_room.html',context)

@login_required(login_url="account:sign_in")
def all_saved_rooms(request):
    user_obj =  User.objects.get(id =  request.user.id)
    all_rooms = Room.objects.filter(approved = True,paid = False)
    all_saved_rooms = SavedRooms.objects.filter(user = user_obj,liked=True)
    min_rent = Room.objects.filter(approved = True,paid = False).annotate(Min('rent')).order_by('rent')[0]
    subtract = len(all_rooms) - 1
    max_rent = Room.objects.filter(approved = True,paid = False).annotate(Max('rent')).order_by('rent')[subtract]
    print("jjj",all_saved_rooms)
    print(max_rent)

    all_similar  = Room.objects.filter(approved = True,paid = False,rent__range = [float(min_rent.rent),float(max_rent.rent)])
    print("similar",all_similar)
    context = {
        'saved_rooms':all_saved_rooms,
        'min_rent':min_rent.rent,
        'max_rent':max_rent.rent,
        'all_similar' :all_similar
        

    }

    return render(request,'all_saved_rooms.html',context)


@login_required(login_url="account:sign_in")
def unsaved_room(request,id):
    get_r = Room.objects.get(id = id)
    user_obj =  User.objects.get(id =  request.user.id)
    print(user_obj)
    obj,created = SavedRooms.objects.get_or_create(room = get_r,user = user_obj)
    obj.liked =  False
    obj.save()
    

    all_saved_rooms = SavedRooms.objects.filter(user = user_obj,liked=True)
    print("jjj",all_saved_rooms)

    context = {
        'saved_rooms':all_saved_rooms
    }



    
    return render(request,'saved_room.html',context)



@login_required(login_url="account:sign_in")
def book_room_payment(request,id):

    specific_room =  Room.objects.get(id =  id)

    context = {
        'specific_room':specific_room
    }
    
    return render(request,'payment_page.html',context)


@login_required(login_url="account:sign_in")
def payment_waiting(request):
    return render(request,'payment_waiting.html')

@login_required(login_url="account:sign_in")
def paid_rooms(request):
    user_obj = User.objects.get(id = request.user.id)
    paid_rooms = BookingRequest.objects.filter(user = user_obj)

    context = {

        'paid_rooms' : paid_rooms

    }
    return render(request,'paid_rooms.html',context)



@login_required(login_url="account:sign_in")
def payment_Processing(request):
    return render(request,'payment_proccessing_c2b.html')

@login_required(login_url="account:sign_in")
def room_detailed_page_paid(request,id):
    
    all_rooms =  Room.objects.get(id = id )
    other_images =  RoomMorePic.objects.filter(room_id =  all_rooms)
    all_rooms_b =  Room.objects.filter(approved = True,paid = False)
    
    print(model_to_dict(all_rooms))
    
    context = {
       
        'rooms_data' :all_rooms,
        'other_images':other_images,
        'all_rooms':all_rooms_b

      
    }
    return render(request,'room_detailed_paid.html',context)

# reviews
# responsive out scroller  and no of images to scrooll,the image should reduce
# paginations on site ..


class SendHTML(APIView):
    def post(self,request):
        plaintext = str(request.data)
        htmly     = get_template('app.html')

        fname =  request.data['fname']
        lname =  request.data['lname']
        sname =  request.data['sname']
        dob =  request.data['dob']
        gender =  request.data['gender']
        knwo_abt_kanzi =  request.data['knwo_abt_kanzi']
        gade_intrested = request.data['gade_intrested']
        email_address =  request.data['email_address']
        contact_info = request.data['contact_info']
        person_inquiring =  request.data['person_inquiring']
        physical_address =  request.data['physical_address']
        mobile_number =  request.data['mobile_number']
        current_school =  request.data['current_school']

        d = {"fname":fname,
        "lname":lname,
        "sname":sname,
        "dob":dob,
        "gender":gender,
        "knwo_abt_kanzi":knwo_abt_kanzi,
        "gade_intrested":gade_intrested,
        "email_address":email_address,
        "contact_info":contact_info,
        "person_inquiring":person_inquiring,
        "physical_address":physical_address,
        "mobile_number":mobile_number,
        "current_school":current_school

        }

        print(d)

        SendEmailKanzi("Student Admission","thomasambetsa@gmail.com","admin@kanzischool.sc.ke",d,htmly,plaintext).start()

        return Response({"success":True})





class SendContactMail(APIView):
    def post(self,request):
        plaintext = str(request.data)
        htmly     = get_template('app_copy.html')

        name =  request.data['name']
        email =  request.data['email']
        message =  request.data['message']
        subject =  request.data['subject']
    
        d = {"fname":name,
        "email":email,
        "message":message,
     
        }

        print(d)

        SendEmailKanzi(f"Inquiry {subject}","thomasambetsa@gmail.com","admin@kanzischool.sc.ke",d,htmly,plaintext).start()
        return Response({"success":True})


@login_required(login_url="account:sign_in")
def map_search_view_authenticated(request):
    
    if request.is_ajax and request.method == "POST":
        user_obj =  User.objects.get(id =  request.user.id)
        sv = SavedRooms.objects.filter(user =  user_obj,liked=True)
       
     
        location =  request.POST.get("location_search")
        building =  request.POST.get('building')
        if(building  == "building"):
            print("checking 1")
          
            
            all_rooms =  Room.objects.filter(approved = True,paid = False,building__building_name =location )
            context= {

                'saved_room':sv,
                'type': building,
                'criteria_mk' : location,
                'formatted' : f"Search for : {location}",
                'all_rooms'  : all_rooms
            }
            
            return render(request,'map.html',context)

        elif (building  == "location"):
            print("checking 2")
            all_rooms =  Room.objects.filter(approved = True,paid = False,building__building_name = location )
            context= {
                'saved_room':sv,
                'type': building,
                'criteria_mk' : location,
                'formatted' : f"Search for : {location}",
                'all_rooms'  : all_rooms
            }
            
            return render(request,'map.html',context)
    all_rooms =  Room.objects.filter(approved = True,paid = False)

    context= {
        'saved_room':sv,
        'rooms' :  all_rooms
    }
    
    return render(request,'fullmap.html',context)



