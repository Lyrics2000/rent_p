
import json
# from django.contrib.gis.geos import Polygon
from fuzzywuzzy import fuzz

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from account.models import  User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Min,Max

from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from homepage.common.CallGlovo import CallGlovo
from homepage.common.CallLeafet import GetLeafletDate
from homepage.common.SendEmailThread import SendEmailThread

from homepage.common.sendsms import sendSms
from homepage.sendEmailT import SendEmailKanzi

from .models import BookingRequest, Building, BuildingMorePic, Coordinated, MapLocations, Room, RoomMorePic, SavedRooms, SlidingImages,BookTour
from .serializers import BuildingSerializer, CoordinatedSerializer, RoomSerializer, SavedRoomSerializers

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from shapely.geometry import Point, Polygon 


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
        
        
        app =  GetLeafletDate(location)
        
        loc= app.get_data()[0]
        osm_id = loc['osm_id']

        js_p = app.getLeafletPolygon()
     
        empty_list_2 = []

        for m in js_p:
             if len(m['geojson']['coordinates']) < 2:
                 empty_list_2.append(m)
        print("jjs",empty_list_2)
    
        if len(empty_list_2) >0:
            geojson = empty_list_2[0]['geojson']['coordinates']
            boundingbox = empty_list_2[0]['boundingbox']
            print("jsp",geojson)
            print("boundingbox",boundingbox)
            
      

        else:
            geojson = []
            boundingbox = []
            print("jsp",geojson)


    
        # print("pp",loc['osm_id'])
        # print("nodes",nodes)
    

        
        rms =  Room.objects.filter(approved = True,paid = False)
        empty_list = []
        for i in rms:
            # if i.building.l_name:
            #     ratio = fuzz.partial_ratio(i.building.l_name.area_name.lower(),location.lower())
            #     if (ratio >=70):
            empty_list.append(i)



        all_rooms =  Room.objects.filter(approved = True,paid = False)
        split_loc = location.split(",")[0]
        if len(boundingbox) > 0:
            context= {
                'boundingbox':boundingbox,
                'main_lat': float(loc['lat']),
                'main_lng': float(loc['lon']),
                'coordinates' : geojson,
                'criteria_mk' : location,
                "xmin":float(boundingbox[0]),
                "xmax":float(boundingbox[1]),
                "ymin" : float(boundingbox[2]),
                "ymax" : float(boundingbox[3]),
                'formatted' : f"Search for : {split_loc}",
                'all_rooms'  : all_rooms
            }
            return render(request,'map_edited.html',context)
        
        else:
            context= {
                
            
                'boundingbox':boundingbox,
                'main_lat': float(loc['lat']),
                'main_lng': float(loc['lon']),
                'coordinates' : geojson,
                'criteria_mk' : location,
                "xmin":float(0),
                "xmax":float(0),
                "ymin" : float(0),
                "ymax" : float(0),
                'formatted' : f"Search for : {split_loc}",
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
      
        criteria_location =  request.data['criteria_location']
        xmin =  request.data['xminm']
        xmax =  request.data['xmaxm']
        ymin =  request.data['yminm']
        ymax =  request.data['ymaxm']

        bbbox = (float(xmin),float(ymin),float(ymax),float(xmax))

        pp =  Polygon.from_bounds(xmin=float(xmin),ymin=float(ymin),xmax=float(xmax),ymax=float(ymax))
        print("oo",pp)
        print("xmin",xmin)
        print("lloo",json.loads(json.dumps((criteria_location))))

        building_filter  = Building.objects.all()
        print("buiding filter",building_filter)
   

        rms =  Room.objects.filter(approved = True,paid = False)
        empty_list = []
        for i in rms:
            for j in building_filter:
                point = Point(j.geom.y,j.geom.x)
                print("point",point)
                if(pp.contains(point)):
                    if(i.building.id) == j.id:

                        point = Point(j.geom.x,j.geom.y)
            # if i.building.l_name:
            #     ratio = fuzz.partial_ratio(i.building.l_name.area_name.lower(),criteria_location.lower())
            #     if (ratio >=70):
                        print("jgeom",j.geom.x,j.geom.y)
                        empty_list.append(i)

        print(empty_list)
        room_serializer =  RoomSerializer(empty_list,many = True)
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

        if max_price == "Maximum Price" and min_price != "Minimum Price":
            print("running 2")
            all_roo =  Room.objects.filter(rent__gte = float(min_price),room_type = beds,approved = True,paid = False)
            serializer = RoomSerializer(all_roo, many=True)
            return Response(serializer.data)
        elif min_price == "Minimum Price" and max_price !="Maximum Price":
            print("running 3")
            all_roo =  Room.objects.filter(rent__lte = float(max_price),room_type = beds,approved = True,paid = False)
            serializer = RoomSerializer(all_roo, many=True)
            return Response(serializer.data)

        elif min_price != "Minimum Price" and max_price !="Maximum Price":
            print("running 4")
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

class SendContactAdminMail(APIView):
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

        SendEmailKanzi(f"Inquiry {subject}","thomasambetsa@gmail.com","admin@ghecko.africa",d,htmly,plaintext).start()
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



class PostLocationCoordinates(APIView):
    def get(self,request):
        all_roomms = Coordinated.objects.all()
        print(all_roomms)
        room_serializer =  CoordinatedSerializer(all_roomms,many = True)
        return Response(room_serializer.data)


    def post(self,request):
        data =  request.data
        features_name = data['features'][0]['properties']['NAME']
        mail_lat = data['features'][0]['properties']['main_lat']
        main_lng = data['features'][0]['properties']['main_lng']

        coordinates = data['features'][0]['geometry']['coordinates']

        obj,created = MapLocations.objects.get_or_create(area_name = features_name )
        obj.main_lat = mail_lat
        obj.main_lng = main_lng
        obj.save()

        for i in coordinates:
            
            for k in i:
                print(k)
                Coordinated.objects.create(
                    map_frame = obj,
                    lat = k[1],
                    lng = k[0]

                )



        
     
        return Response({"success":"ok"})




class CallGlovoAPiview(APIView):
    def post(self,request):
        data =  request.data['name']
        app = CallGlovo(data)
        resp =  app.request_data()
        return Response(resp)



class FilterWithCurrentLocation(APIView):
    def get(self,request):
        criteria = request.query_params
        print(criteria)
        all_roomms = Room.objects.filter(approved = True,paid = False)
        room_serializer =  RoomSerializer(all_roomms,many = True)
        return Response(room_serializer.data)


    def post(self,request):
      
        latitude =  request.data['lat']
        longitude = request.data['lon']
        room_type = request.data['room_type']
        print("room type",room_type)

        app = GetLeafletDate("nairobi").leafletReverse(lat=latitude,lon=longitude)
        print("app",app)
        boundingbox = app[0]['boundingbox']
        print("bounding box",boundingbox)

        xmin  = float(boundingbox.split(",")[0])
        xmax = float(boundingbox.split(",")[1])
        ymin   = float(boundingbox.split(",")[2])
        ymax = float(boundingbox.split(",")[3])

   
        pp =  Polygon.from_bounds(xmin=float(xmin),ymin=float(ymin),xmax=float(xmax),ymax=float(ymax))
        print("oo",pp)
        print("xmin",xmin)

        building_filter  = Building.objects.all()
        print("buiding filter",building_filter)
   

        rms =  Room.objects.filter(approved = True,paid = False,room_type__contains = room_type)
        empty_list = []
        for i in rms:
            for j in building_filter:
                point = Point(j.geom.y,j.geom.x)
                print("point",point)
                if(pp.contains(point)):
                    if(i.building.id) == j.id:

                        point = Point(j.geom.x,j.geom.y)
         
                        print("jgeom",j.geom.x,j.geom.y)
                        empty_list.append(i)

        print(empty_list)
        room_serializer =  RoomSerializer(empty_list,many = True)
        return Response(room_serializer.data)






