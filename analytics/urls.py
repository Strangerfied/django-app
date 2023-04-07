from django.urls import path
from analytics.views import MaxRain
from . import views

urlpatterns = [
    path("api/analytics/", MaxRain),
    ]
