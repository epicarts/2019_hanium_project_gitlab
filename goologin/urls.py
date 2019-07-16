from django.contrib import admin
from django.urls import path,include
from . import views
import goologin.views

urlpatterns=[
    path('googlelogin/',include('allauth.urls')),
    path('',views.home,name='home'),
]
