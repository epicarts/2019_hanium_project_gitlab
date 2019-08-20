# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
import json
from .models import Room
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import Group
import os
from django.conf import settings 

'''
from django.contrib.auth.decorators import permission_required

@permission_required('deals.can_invest')
def my_view(request):

has_perm() 함수와 동일하게, . 과 같이 지정하면 된다. `permission_required()` 함수 또한 `login_url` 를 인자로 받을 수 있으며, `raise_exception`이 주어지면, `PermissionDenied` 에러가 발생하며 로그인 페이지로 이동하는 대신 403에러 페이지를 보여주게 된다.
'''

def room_delete(request, room_pk):
    #방 삭제 검증 한번 더. 
    perimssion_codename_del = 'main.room_'+ str(room_pk) +'_delete'
    if request.user.has_perm(perimssion_codename_del):
        room = Room.objects.get(pk = room_pk)

        #업로드한 파일이 존재하면 삭제.
        if room.uploadfile:
            os.remove(os.path.join(settings.MEDIA_ROOT, room.uploadfile.path))
        
        #그룹 및 권한 삭제 추가 예정

        #데이터 베이스 삭제.
        room.delete()
        return redirect('main:RoomList')


@login_required
def room(request, room_pk):
    '''
    GET
    1. 현재 유저가 펴미션이 있나 체크
    2. 권한 있음: 룸 입장
    3. 권한 없음: redirect 후 패스워드 입력

    POST
    1. 패스워드 요청이 들어오면 체크(POST)
    2. 패스워드가 맞다:  그룹에 속하게 함(그룹 has 권한)
    3. 패스워드가 다르다: redirect 후 패스워드 틀림페이지
    '''
    if request.method == 'GET':
        #현재 로그인 되어있는 계정을 기준으로 퍼미션 체크를 한다.
        perimssion_codename = 'main.room_'+ str(room_pk) +'_view'

        #퍼미션을 가지고 있다면 정상적으로 페이지를 보여줌
        if request.user.has_perm(perimssion_codename):
            room = Room.objects.get(pk=room_pk)
            room_messages = reversed(room.messages.order_by('-timestamp')[:5])
            
            perimssion_codename_del = 'main.room_'+ str(room_pk) +'_delete'
            perimssion_del =False
            if request.user.has_perm(perimssion_codename_del):
                perimssion_del = True

            return render(request, 'chat/room.html', {
                'room_pk_json': mark_safe(json.dumps(room_pk)),
                'messages':room_messages,
                'room':room,
                'perimssion_del':perimssion_del,
            }) 
        else:#처음 방 입장을 하면 패스워드가 없으므로 패스워드 입력 페이지를 랜더링
            messages.add_message(request, messages.INFO, room_pk)#request에 message 추가
            return redirect('main:RoomList')

    elif request.method == 'POST': #패스워드 인증 요청이 패스워드 입력 페이지로부터 AJAX 요청이 들어오면 
        print('post request BY AJAX')
        if request.POST['password'] == Room.objects.get(pk=room_pk).password:# 파라미터로 입력받은 값을 방의 패스워드와 비교함 ,
            #접속한 유저를 패스워드를 통과한 방 그룹에 속하게 함.
            groupname = 'room_'+ str(room_pk) +'_group'
            new_group = Group.objects.get(name=groupname) 
            request.user.groups.add(new_group)
            # 200 == success, 리다이렉션 처리는 js에서 함
            #messages.add_message(request, messages.INFO, room_pk)#request에 message 추가
            print("인증 성공",room_pk)
            return JsonResponse({
                'message' : '인증에 성공하였습니다.', 
            }) # http status 200
            
        else:#패스워드가 다르면 리다이렉트...
            return JsonResponse({
                'message' :'패스워드가 잘못 되었습니다.',
            }, status=400) #  http status 400 잘못된 패스워드, 리다이렉션 처리는 js에서 함