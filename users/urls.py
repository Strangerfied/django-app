from users.views import Users
from django.urls import path
from . import views
from django.urls import register_converter
from datetime import datetime
from django.contrib.auth import views as auth_views

class DateTimeConverter:
    regex = "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}\+[0-9]{2}:[0-9]{2}"

    def to_python(self, value):
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f+%z")

    def to_url(self, value):
        return value.isoformat()


urlpatterns = [
        path("users/", Users),
        ]
