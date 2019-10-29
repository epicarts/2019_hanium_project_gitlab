"""hanium URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
import goologin.views
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    #accounts 로 접속시 accounts.urls.py 포함
    path('accounts/', include('accounts.urls'), ),
    path('room/',include('chat.urls')),
    path('googlelogin/',include('allauth.urls')),
    path('',include('main.urls')),
    url(r'^media/(?P<path>.*)$',serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#from django.conf.urls import(handler404)
#handler404='django.views.page_not_found'

