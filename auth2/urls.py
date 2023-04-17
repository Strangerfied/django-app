from django.urls import path
from auth2.views import login
from auth2.views import logout
app_name = 'auth2'

urlpatterns = [
    path('accounts/login/', login, name='login'),
    path('logout/', logout),
]
