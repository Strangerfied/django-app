from django.urls import path
from weather.views import Weather
#from weather.views import GetTemperatures
#from weather.views import IndexQuery
from django.urls import register_converter
from datetime import datetime
from django.contrib.auth import views as auth_views
from weather.views import ConnectionTest
#tei

class DateTimeConverter:
    regex = "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}\+[0-9]{2}:[0-9]{2}"

    def to_python(self, value):
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f+%z")

    def to_url(self, value):
        return value.isoformat()


register_converter(DateTimeConverter, "datetime")

urlpatterns = [
    #path("", views.index, name="index"),
    # path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    path("weather/", Weather),
    #path("weather/batch/", GetTemperatures, name="batch"),
    #path("weather/index/", IndexQuery),
    path('connectiontest/', ConnectionTest, name='ConnectionTest'),
    ]


