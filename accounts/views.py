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

class RegisterView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = RegistrationFrom()
        return render(request,'registration/register.html' , context={'form':form} )


    def post(self, request, *args, **kwargs):
        form = RegistrationFrom(request.POST)
        if form.is_valid():
            if form.cleaned_data['password2']  == form.cleaned_data['password1']:
                if User.objects.filter(username=form.cleaned_data['username']).exists():
                    form.add_error('username', '이미 사용중인 아이디 입니다.')
                else:
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password1']
                    )
                    return HttpResponseRedirect('/')#회원가입 완료시 리다이렉트 되는 
            else:
                form.add_error('password2', '패스워드가 일치하지 않습니다.')

# @login_required#로그인 데커레이터, 이게 붙어있는 함수는 반드시 로그인을 해야함. 하지 않으면 로그인 경로로 이동
# def profile(request):
#     data = {'last_login': request.user.last_login, 'username': request.user.username,
#             'password': request.user.password, 'is_authenticated': request.user.is_authenticated}
#     return render(request, 'accounts/profile.html', context={'data': data})

# def profile(request):
#     if not request.user.is_authenticated:#인증되지 않았다면
#         data = {'username': request.user, 'is_authenticated': request.user.is_authenticated}
#     else:
#         data = {'last_login': request.user.last_login, 'username': request.user.username,
#                 'password': request.user.password, 'is_authenticated': request.user.is_authenticated}
#     return render(request, 'accounts/profile.html', context={'data': data})
#
#클래스로 만듦. Mixin 를 사용해야함. 클래스 이하에 있는 모든 함수는 로그인이 반드시 필요.
class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = {'last_login': request.user.last_login, 'username': request.user.username,
                'password': request.user.password, 'is_authenticated': request.user.is_authenticated}
        return render(request, 'accounts/profile.html', context={'data': data})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # cleaned_data로 관련 로직 처리
            return HttpResponseRedirect('/success/')
        return render(request, self.template_name, {'form':form})