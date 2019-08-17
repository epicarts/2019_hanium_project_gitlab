from django.shortcuts import render,redirect
from django.views import View
from .models import Room
from django.contrib.auth.decorators import login_required
from .forms import CreateMain

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

from django.core.signing import Signer

from django import template

import datetime
from django import template

from django.contrib import messages

# Create your views here.
@login_required
def main(request):
    RoomList=reversed(Room.objects.all()) #가장 최근에 만들어진 방을 위로 정렬..
    return render(request, 'main/main.html', {'RoomList':RoomList})

@login_required
def createMain(request):
    if request.method == 'POST':
        form = CreateMain(request.POST)
        if form.is_valid():#폼 형식이 맞으면
            #cleaned_data는 사용자가 입력한 데이터를 뜻한다.
            if form.cleaned_data['password']  == form.cleaned_data['confirm_password']:
                post = form.save(commit=False) # 함수 호출 지연
                post.author = request.user # 유저 id 필드는 유저로 부터 입력 받지 않고 프로그램으로 채워 넣는다
                post.save()
                '''
                그룹 및 권한 추가
                그룹: room_{pk}_group
                권한: room_{pk}_view  / room_{pk}_delete
                '''
                groupname = 'room_'+ str(post.pk) +'_group'
                #그룹이 없다면 생성하거나 가져옴. 그룹 이름은 방을 생성할 때 방 그룹은 id room_id 
                new_group, created = Group.objects.get_or_create(name=groupname)
                #그룹에 권한(permission 생성 및 추가)
                perimssion_codename = 'room_'+ str(post.pk) +'_view'
                perimssion_name = 'Can view Room ' + str(post.pk) 
                content_type = ContentType.objects.get(app_label='main', model='Room')
                permission = Permission.objects.create(codename=perimssion_codename, name=perimssion_name, content_type=content_type)
                new_group.permissions.add(permission)#그룹에 권한 추가
                request.user.groups.add(new_group)#그룹에 개인 추가

                # Code to add permission to group 
                # room 모델을 삭제할 수 있는 permission을 만듬
                perimssion_codename = 'room_'+ str(post.pk) +'_delete'
                perimssion_name = 'Can delete Room ' + str(post.pk) 
                content_type = ContentType.objects.get(app_label='main', model='Room')
                permission = Permission.objects.create(codename=perimssion_codename, name=perimssion_name, content_type=content_type)
                request.user.user_permissions.add(permission)#방 생성한 사람에게 권한을 줌

                #redirect('/detail/'+str(cat.pk)) 저장하고 만들어진 페이지로
                return redirect('main:RoomList')#저장하고 main으로 
            else:##password와 password_check가 다를 것을 대비하여 error를 지정해준다.
                messages.add_message(request, messages.INFO, "패스워드가 알치하지 않습니다.")
                return redirect('main:createMain')

        else:#폼 형식이 맞지 않으면 맞지 않으면 메시지와 redirect
            messages.add_message(request, messages.INFO, "폼 형식이 맞지 않습니다. 다시 입력해 주세요.")
            return redirect('main:createMain')

    if request.method == 'GET': # GET일 경우 form을 상속받아서, createMain.html로 전달
        form = CreateMain()
        return render(request,'main/createMain.html',{"form":form})