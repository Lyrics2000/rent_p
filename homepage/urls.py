

from django.urls import path
from djgeojson.views import GeoJSONLayerView
from .models import Building,Room
from .views import (
    index,
    map_search_view,
    GetBUildingAPIVIEW,
    GetRoom,
    map_detailed_page,
    FilterRoom
)

app_name = "homepage"
urlpatterns = [
    path('', index,name="homepage"),
    path('map_search',map_search_view,name="map_search"),
    path("all_buildings/",GeoJSONLayerView.as_view(model=Building,properties=('agent','building_name','no_of_floors','no_of_Room','location_name','parking_space','security','tv_connection','account_number','owner','payment_deadline','penalties','approved','created')),name="all_buildings"),
    path('get_all_data/',GetBUildingAPIVIEW.as_view(),name="get_all_data"),
    path('room_name/',GetRoom.as_view(),name="get_room"),
    path('map_detailed/<id>/',map_detailed_page,name="map_detailed"),
    path('filter_room/',FilterRoom.as_view(),name="filtered_data")
  
]

