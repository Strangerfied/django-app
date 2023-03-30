# myapi/urls.py
#test
from django.urls import path
from myapi.views import TheModelView
from myapi.views import WeatherStation
from myapi.views import Users
from myapi.views import WeatherData
from myapi.views import MaxRain
from myapi.views import GetTemperatures
from myapi.views import IndexQuery
from myapi.views import delete_user
from myapi.views import delete_users
from myapi.views import update_weather_station
from myapi.views import update_access_level
from myapi.views import AddFahrenheitTemps
#from rest_framework import routers
from . import views
from django.urls import register_converter
from datetime import datetime

#router = routers.DefaultRouter()
#router.register(r'heroes', views.HeroViewSet)

class DateTimeConverter:
    regex = '[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}\+[0-9]{2}:[0-9]{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f+%z')

    def to_url(self, value):
        return value.isoformat()

register_converter(DateTimeConverter, 'datetime')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('',views.index,name='index'),
   # path('', include(router.urls)),
   # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    path('themodel/', TheModelView),
    path('weatherstation/', WeatherStation),
    path('users/', Users),
    path('weatherdata/', WeatherData),
    path('maxrain/', MaxRain),
    path('addfahrenheit/', AddFahrenheitTemps, name='add_fahrenheit_temps'),
    path('stationdata/<str:station_name>/<str:date_time>/', views.GetStationData, name='get_station_data'),
    path('gettemps/', GetTemperatures, name='batch'),
    path('indexquery/<int:index_value>/', IndexQuery),
    path('users/<str:user_name>/', delete_user, name='delete_user'),
    path('usersdelete/', delete_users, name='delete_users'),
    path('weather-stations/<str:station_id>/', update_weather_station, name='update_weather_station'),
    path('usersupdate/update_access_level/', update_access_level, name='update_access_level')
    ]
