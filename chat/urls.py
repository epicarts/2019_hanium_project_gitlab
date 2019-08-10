# chat/urls.py
from django.conf.urls import url
from django.urls import path
from . import views

app_name='room'

urlpatterns = [
    path('<str:room_name>/', views.room, name='room_detail'),
]
