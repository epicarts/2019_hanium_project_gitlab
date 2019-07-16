from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


#namespace
app_name='main'


urlpatterns = [
    #로그인 성공 시 => profile로 리다이텍트 됨 settings
    path('', views.main),
]
