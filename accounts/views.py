from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from accounts.forms import RegistrationFrom
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User

class IndexView(View):
    def get(self, request, *args, **kwargs):
        context = {'parm1': 'hello', 'parm2': 'django', 'auth': request.user.is_authenticated}
        print(request.user)
        return render(request, 'index.html', context=context)


# Create your views here.
def hello(request):
    print(request)
    return render(request, 'accounts/hello.html', {'title': 'hello accounts page', 'body': 'world'})

def register_page(request):
    if request.method == 'POST':
        form = RegistrationFrom(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            return HttpResponseRedirect('/')#회원가입 완료시 리다이렉트 되는 곳
    else:
        form = RegistrationFrom()

    return render(request,'registration/register.html' , context={'form':form} )


@login_required#로그인 데커레이터, 이게 붙어있는 함수는 반드시 로그인을 해야함. 하지 않으면 로그인 경로로 이동
def profile(request):
    data = {'last_login': request.user.last_login, 'username': request.user.username,
            'password': request.user.password, 'is_authenticated': request.user.is_authenticated}
    return render(request, 'accounts/profile.html', context={'data': data})

# def profile(request):
#     if not request.user.is_authenticated:#인증되지 않았다면
#         data = {'username': request.user, 'is_authenticated': request.user.is_authenticated}
#     else:
#         data = {'last_login': request.user.last_login, 'username': request.user.username,
#                 'password': request.user.password, 'is_authenticated': request.user.is_authenticated}
#     return render(request, 'accounts/profile.html', context={'data': data})
#
#클래스로 만듦. Mixin 를 사용해야함. 클래스 이하에 있는 모든 함수는 로그인이 반드시 필요.
# class ProfileView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         data = {'last_login': request.user.last_login, 'username': request.user.username,
#                 'password': request.user.password, 'is_authenticated': request.user.is_authenticated}
#         return render(request, 'profile.html', context={'data': data})
