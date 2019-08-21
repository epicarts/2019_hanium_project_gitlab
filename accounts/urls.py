from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


#namespace
app_name='accounts'


urlpatterns = [
    # redirect_authenticated_user 로그인 되어 있으면 접근 불가...!!!
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('password/change/', views.PasswordChange.as_view(), name='password_change'),

    #127.0.0.1/accounts 뒤에 아무것도 없을때
    #path('', views.PostList.as_view())
]
