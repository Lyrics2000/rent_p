

from unicodedata import name
from django.urls import path
from djgeojson.views import GeoJSONLayerView
from .models import Building,Room
from .views import (
    index,
    map_search_view,
    GetBUildingAPIVIEW,
    GetRoom,
    map_detailed_page,
    FilterRoom,
    room_detailed_page,
    request_booking,
    listing_listview,
    book_request,
    saved_room,
    FilterSavedRoom,
    all_saved_rooms,
    unsaved_room
)

app_name = "homepage"
urlpatterns = [
    path('', index,name="homepage"),
    path('map_search',map_search_view,name="map_search"),
    path("all_buildinunsaved_roomgs/",GeoJSONLayerView.as_view(model=Building,properties=('agent','building_name','no_of_floors','no_of_Room','location_name','parking_space','security','tv_connection','account_number','owner','payment_deadline','penalties','approved','created')),name="all_buildings"),
    path('get_all_data/',GetBUildingAPIVIEW.as_view(),name="get_all_data"),
    path('room_name/',GetRoom.as_view(),name="get_room"),
    path('map_detailed/<id>/',map_detailed_page,name="map_detailed"),
    path('filter_room/',FilterRoom.as_view(),name="filtered_data"),
    path('room_detailed/<id>/',room_detailed_page,name="room_detailed"),
    path('booking_request/<room_id>/<agent_id>/<user_id>/',request_booking,name="request_booking"),
    path('listing_listview/',listing_listview,name="listing_listview"),
    path('book_request/<id>/',book_request,name="book_request"),
    path('saved_rentals/<id>/',saved_room,name="saved_rentals"),
    path('filter_saved_rooms/',FilterSavedRoom.as_view(),name="filter_saved_rooms"),
    path('all_saved_rooms/',all_saved_rooms,name="all_saved_rooms"),
    path('unsaved_room/<id>/',unsaved_room,name="unsaved_rentals")

  
]

