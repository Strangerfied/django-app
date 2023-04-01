from django.urls import path
from stations.views import WeatherStation
from . import views


urlpatterns = [
    path("stations/", WeatherStation),
    ]
