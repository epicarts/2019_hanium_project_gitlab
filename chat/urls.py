# chat/urls.py
from django.conf.urls import url
from django.urls import path
from . import views

app_name='chat'

urlpatterns = [
    path('<str:room_pk>/', views.room, name='room_detail'),
    path('<str:room_pk>/delete/', views.room_delete, name='room_delete'),
]