

from unicodedata import name
from django.urls import path
from djgeojson.views import GeoJSONLayerView
from .models import Building,Room
from .views import (
    CallGlovoAPiview,
    FilterWithCurrentLocation,
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
    unsaved_room,
    book_room_payment,
    payment_waiting,
    paid_rooms,
    payment_Processing,
    room_detailed_page_paid,
    SendHTML,
    SendContactMail,
    GetRoomAl,
    map_search_view_authenticated,
    PostLocationCoordinates,
    SendContactAdminMail,
    GetCoordinatesAndBounds
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
    path('room_detailed_paid/<id>/',room_detailed_page_paid,name="room_detailed_page_paid"),

    path('booking_request/<room_id>/<agent_id>/<user_id>/',request_booking,name="request_booking"),
    path('listing_listview/',listing_listview,name="listing_listview"),
    path('book_request/<id>/',book_request,name="book_request"),
    path('saved_rentals/<id>/',saved_room,name="saved_rentals"),
    path('filter_saved_rooms/',FilterSavedRoom.as_view(),name="filter_saved_rooms"),
    path('all_saved_rooms/',all_saved_rooms,name="all_saved_rooms"),
    path('unsaved_room/<id>/',unsaved_room,name="unsaved_rentals"),
    path('booking_payment/<id>/',book_room_payment,name="book_room_payment"),
    path("payment_waiting/",payment_waiting,name="payment_waiting"),
    path("paid_rooms/",paid_rooms,name="paid_rooms"),
    path("payment_Processing/",payment_Processing,name="payment_Processing"),
    path("send_mail/kanzi/",SendHTML.as_view()),
    path("send_email_contact_kanzi/",SendContactMail.as_view()),
    path("get_all_rooms/",GetRoomAl.as_view(),name="all_rm"),
    path("map_search_view_authenticated/",map_search_view_authenticated,name="map_search_view_authenticated"),
    path("post_location_coordinates/",PostLocationCoordinates.as_view()),
    path("send_em/",SendContactAdminMail.as_view()),
    path('call_glovo/',CallGlovoAPiview.as_view(),name="call_glovo"),
    path("search_with_lat/",FilterWithCurrentLocation.as_view(),name="search_with_lat_and_lon"),
    path("get_coordinates_and_bounds/",GetCoordinatesAndBounds.as_view(),name="get_coordinates_and_bounds")

  
]

