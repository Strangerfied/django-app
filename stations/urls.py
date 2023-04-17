from django.urls import path
from stations.views import Stations
from . import views
from django.contrib.auth import views as auth_views
from django.urls import register_converter
from datetime import datetime
#from django.contrib.auth import views as auth_views
from weather.views import ConnectionTest


class DateTimeConverter:
    regex = "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}\+[0-9]{2}:[0-9]{2}"

    def to_python(self, value):
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f+%z")

    def to_url(self, value):
        return value.isoformat()


register_converter(DateTimeConverter, "datetime")


urlpatterns = [
    path("api/stations/", Stations),
    ]
