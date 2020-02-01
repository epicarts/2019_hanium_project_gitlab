from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


#namespace
app_name='main'


urlpatterns = [
    #로그인 성공 시 => profile로 리다이텍트 됨 settings
    path('', views.main, name='RoomList'),
    #path('seo/',views.seo,name='seo'),
    path('createMain/',views.createMain,name='createMain'),
    path('webcam/',views.webcam, name='webcam'),

#    path('imroom/',views.imroom,name='imroom'),
]

#from django.conf.urls import(handler404)

#handler404='django.views.page_not_found'