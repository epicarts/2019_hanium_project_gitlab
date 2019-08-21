from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


#namespace
app_name='accounts'


urlpatterns = [
    #로그인 성공 시 => profile로 리다이텍트 됨 settings
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('', views.hello),
    path('register/', views.RegisterView.as_view(), name='register'),

    #127.0.0.1/accounts 뒤에 아무것도 없을때
    #path('', views.PostList.as_view())
]
