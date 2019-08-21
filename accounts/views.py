from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from accounts.forms import RegistrationFrom, PasswordChangeFrom


from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User

from django.contrib.auth.hashers import check_password
from django.contrib import messages

from django.contrib.auth import authenticate, login

class IndexView(View):
    def get(self, request, *args, **kwargs):
        context = {'parm1': 'hello', 'parm2': 'django', 'auth': request.user.is_authenticated}
        print(request.user)
        return render(request, 'index.html', context=context)


# Create your views here.
def hello(request):
    print(request)
    return render(request, 'accounts/hello.html', {'title': 'hello accounts page', 'body': 'world'})

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        print('RegisterView access')
        form = RegistrationFrom()
        return render(request,'registration/register.html' , context={'form':form} )


    def post(self, request, *args, **kwargs):
        print('RegisterView access')
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
        return render(request,'registration/register.html' , context={'form':form} )

class ProfileView(LoginRequiredMixin, View):
    '''
    마이페이지(프로파일) 보는 페이지
    '''
    def get(self, request, *args, **kwargs):
        data = {'last_login': request.user.last_login, 'username': request.user.username}
        return render(request, 'accounts/profile.html', context={'data': data})

class PasswordChange(LoginRequiredMixin, View):
    '''
    패스워드 수정하는 페이지
    '''
    def get(self, request, *args, **kwargs):
        form = PasswordChangeFrom()
        data = {'last_login': request.user.last_login, 'username': request.user.username}
        return render(request, 'accounts/password_change.html', context={'data': data, 'form': form})

    def post(self, request, *args, **kwargs):
        '''
        패스워드 변경 요청이 들어오면...
        1. 현재 패스워드와 같은지 검사
        2. 새 패스워드와 새 패스워드 확인이 같은지 검사
        3. 각각에 상황에 맡는 값을 message 에 담아서 리턴
        '''
        context = {}
        form = PasswordChangeFrom(request.POST)
        if form.is_valid():# 폼형식이 맞으면,
            if check_password(form.cleaned_data['current_password'],request.user.password):
                #1. 현재 패스워드와 같은지 검사
                print("현재 패스워드와 같음.")
                new_password = form.cleaned_data['new_password']
                confirm_new_password = form.cleaned_data['confirm_new_password']
                if new_password  == confirm_new_password:#2. 새 패스워드와 새 패스워드 확인이 같은지 검사
                    request.user.set_password(new_password)
                    request.user.save()

                    #패스워드 변경후 자동 로그인
                    user = authenticate(request, username=request.user, password=new_password)
                    login(request, user)
                    messages.add_message(request, messages.INFO, "성공적으로 변경되었습니다.")
                else:
                    messages.add_message(request, messages.ERROR, "새로운 비밀번호를 다시 확인해주세요.")
            else:
                print("현재 패스워드와 다름.")
                messages.add_message(request, messages.ERROR, "현재 비밀번호가 일치하지 않습니다.")

        return redirect('accounts:password_change')