# myapi/urls.py
# test
from django.urls import path
from myapi.views import TheModelView
from myapi.views import WeatherStation
from myapi.views import Users
from myapi.views import WeatherData
from myapi.views import MaxRain
from myapi.views import GetTemperatures
from myapi.views import IndexQuery
from myapi.views import update_weather_station
from myapi.views import update_access_level
from myapi.views import AddFahrenheitTemps

# from rest_framework import routers
from . import views
from django.urls import register_converter
from datetime import datetime
from django.contrib.auth import views as auth_views

# router = routers.DefaultRouter()
# router.register(r'heroes', views.HeroViewSet)


class DateTimeConverter:
    regex = "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}\+[0-9]{2}:[0-9]{2}"

    def to_python(self, value):
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f+%z")

    def to_url(self, value):
        return value.isoformat()


register_converter(DateTimeConverter, "datetime")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", views.index, name="index"),
    # path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    path("themodel/", TheModelView),
    path("weatherstation/", WeatherStation),
    path("api/users/", Users),
    path("weatherdata/", WeatherData),
    path("api/maxPrecipitation/", MaxRain),
    path("api/fahrenheit/", AddFahrenheitTemps, name="add_fahrenheit_temps"),
    path("api/stationData/", views.GetStationData, name="get_station_data"),
    path("gettemps/", GetTemperatures, name="batch"),
    path("indexquery/<int:index_value>/", IndexQuery),
    # path("api/users/", delete_users, name="delete_users"),
    path(
        "api/stations/",
        update_weather_station,
        name="update_weather_station",
    ),
    path(
        "usersupdate/update_access_level/",
        update_access_level,
        name="update_access_level",
    ),
    path('login/', auth_views.LoginView.as_view(), name='login'),
]
