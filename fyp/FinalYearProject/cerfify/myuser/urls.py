from django.urls import path
from . import views

app_name= "myuser"
urlpatterns = [
    path('register/',views.register,name='myuser_register'),
    path('profile/',views.profile,name='myuser_profile')
]

