# from django.db import models
from email.charset import BASE64
from operator import mod
from pyexpat import model
import random
import os
from statistics import mode
from urllib import request
from django.shortcuts import reverse
from account.models import User,Agent
from location_field.models.plain import PlainLocationField
from djgeojson.fields import PolygonField
from django.contrib.gis.db import models


# Create your models here.

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name,ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance,filename):
    new_filename = random.randint(1,999992345677653234)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext = ext)
    return "thumbnails/{new_filename}/{final_filename}".format(new_filename=new_filename,final_filename = final_filename )

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MapLocations(models.Model):
    area_name = models.CharField(max_length=255)
    main_lat = models.CharField(max_length=255)
    main_lng = models.CharField(max_length=255)


    def __str__(self):
        return self.area_name


class Building(BaseModel):
    agent =  models.ForeignKey(Agent,on_delete=models.CASCADE,help_text="This email of the agent")
    building_name = models.CharField(max_length=255,help_text="The building name")
    no_of_floors =  models.IntegerField(help_text="Number of floors of the building")
    no_of_Room =  models.IntegerField(help_text="Number of rooms in the whole building")
    l_name =  models.ForeignKey(MapLocations,on_delete=models.CASCADE,help_text="The location name of the building",blank=True,null=True)
   
    geom = models.PointField(srid=4326,blank=True,null=True)
    parking_space =  models.CharField(max_length=255,help_text="The parking size of the building example 10000 sqm")
    security =  models.BooleanField(default=False,help_text="if true means the building has security example: cctv,guars")
    tv_connection =  models.BooleanField(default=False,help_text="if true the building has tv connections cables")
    account_number =  models.CharField(max_length=255,help_text="The account number for rent payment for the building")
    payment_instructions = models.TextField(blank=True,null=True,help_text="Payment Instructions")
    owner =  models.CharField(max_length=255,help_text="The name of the owner of the building")
    description = models.TextField(blank=True,null=True,help_text="The description of the building")
    payment_deadline =  models.DateField(help_text="The payment deadline when rent is due")
    penalties =  models.CharField(max_length=255,help_text="penalties for late rent payment")
    building_main_pic =  models.ImageField(upload_to = upload_image_path,help_text="The building picture")
    # featured =  models.BooleanField(default=False)
    approved =  models.BooleanField(default=False,help_text="This helps us to know if the building can appear on site or not ")


    def __str__(self):
        return self.building_name

    def get_absolute_url(self):
        return reverse("homepage:map_detailed", kwargs={
            'id': self.id
        })

    
ROOM_TYPES = (
    ('Single Room', 'Single Room'),
    ('Double Room', 'Double Room'),
    ('BedSitter', 'BedSitter'),
    ('1 Bedroom', '1 Bedroom'),
    ('2 Bedroom', '2 Bedroom'),
    ('3 Bedroom', '3 Bedroom'),
    ('4 Bedroom', '4 Bedroom'),
    )



class Room(BaseModel):
    building =  models.ForeignKey(Building,on_delete=models.CASCADE,help_text="The building name")
    room_name =  models.CharField(max_length=255,help_text="The name of the room or house number example AB1")
    room_type =  models.CharField(choices=ROOM_TYPES, max_length=50,help_text="The type of the room example single room")
    rent =  models.DecimalField(max_digits=20,decimal_places=2,help_text="The total amount of rent per month")
    deposit = models.DecimalField(max_digits=20,decimal_places=2,help_text="The total first time deposite exclusive of the rent") 
    floor =  models.IntegerField(help_text="The floor number of the room ")
    bathtab_np =  models.IntegerField(help_text="The number of bathtab for the room if non input 0 ")
    balcony =  models.BooleanField(default=False,help_text="if true means the room has a balcony ")
    room_size =  models.CharField(max_length=255,help_text="The total area in room example 1000sqm ")
    description = models.TextField(blank=True,null=True,help_text="The description of the room")
    room_picture =  models.ImageField(upload_to = upload_image_path,help_text="The picture of the room ")
    # featured =  models.BooleanField(default=False)
    room_video = models.FileField(upload_to = upload_image_path,help_text="The video of room ",blank=True,null=True)
    approved =  models.BooleanField(default=False,help_text="if true means the room can appear on site ")
    paid = models.BooleanField(default=False)
    
    def __str__(self):
        return self.room_name


    def get_absolute_url(self):
        return reverse("homepage:room_detailed", kwargs={
            'id': self.id
        })

    def get_absolute_room_paid_detailed_url(self):
        return reverse("homepage:room_detailed_page_paid", kwargs={
            'id': self.id
        })


    def get_book_request(self):
        return reverse("homepage:book_request", kwargs={
            'id': self.id
        })

        # book_room_payment

    def get_book_payment(self):
        return reverse("homepage:book_room_payment", kwargs={
            'id': self.id
        })

    def get_saved_rentals(self):
        return reverse("homepage:saved_rentals", kwargs={
            'id': self.id
        })

    def get_unsaved_rentals(self):
        return reverse("homepage:unsaved_rentals", kwargs={
            'id': self.id
        })


    



class RoomMorePic(BaseModel):
    room_id =  models.ForeignKey(Room,on_delete=models.CASCADE,help_text="The room name")
    image =  models.ImageField(upload_to=upload_image_path,help_text="More pictures of the room ")

    def __str__(self):
        return str(self.room_id)


class Booking(BaseModel):
    building =  models.ForeignKey(Building,on_delete=models.CASCADE,help_text="The  name of the building ")
    property_manager =  models.ForeignKey(Agent,on_delete=models.CASCADE,help_text="The property manager for the buidling")
    user =  models.ForeignKey(User,on_delete=models.CASCADE,blank = True,null =  True,help_text="The user id for the building ")
    room =  models.ForeignKey(Room,on_delete=models.CASCADE,help_text="The room name ")
    booking_status =  models.BooleanField(default=False,help_text="if true it means the room is paid for and hence considered booked ")

    def __str__(self):
        return str(self.building_id)

class Payment(BaseModel):
    booking_id =  models.ForeignKey(Building,on_delete=models.CASCADE)
    amount_paid =  models.DecimalField(max_digits=20,decimal_places=2)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False)
    payment_type =  models.CharField(max_length=255)

    def __str__(self):
        return str(self.booking_id)


class BuildingMorePic(BaseModel):
    building_id = models.ForeignKey(Building,on_delete=models.CASCADE)
    image =  models.ImageField(upload_to = upload_image_path)

    def __str__(self):
        return str(self.building_id)



class SlidingImages(BaseModel):
    images =  models.ImageField(upload_to = upload_image_path)


class BookTour(BaseModel):
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    day = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    reviewed = models.BooleanField(default=False)


    def __str__(self):
        return str(self.email)



class SavedRooms(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)


    def __str__(self):
        return str(self.user)


class BookingRequest(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    contact_phone = models.CharField(max_length=255)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.name





class Coordinated(models.Model):
    map_frame = models.ForeignKey(MapLocations,on_delete=models.CASCADE)
    lat = models.CharField(max_length=255)
    lng = models.CharField(max_length=255)

    def __str__(self):
        return str(self.map_frame)







