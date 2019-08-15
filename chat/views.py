# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
import json
from .models import Room
from django.utils import timezone
from django.contrib import messages

# def index(request):
#     return render(request, 'chat/index.html', {})

# @login_required
# def new_room(request, room_name):
#     return redirect(room,label='새로 만들 방 이름을 라벨로...')
'''
from django.contrib.auth.decorators import permission_required

@permission_required('deals.can_invest')
def my_view(request):

has_perm() 함수와 동일하게, . 과 같이 지정하면 된다. `permission_required()` 함수 또한 `login_url` 를 인자로 받을 수 있으며, `raise_exception`이 주어지면, `PermissionDenied` 에러가 발생하며 로그인 페이지로 이동하는 대신 403에러 페이지를 보여주게 된다.
'''
# from django.contrib.auth.decorators import user_passes_test

# def email_check(user):
#     return user.email.endswith('@example.com')

# #룸에 대한 pk 값을 체크. + 해당 pk에 대해 권한이 있는지 체크. 
# #만약 권한이 없다면, 페이지를 보여 줄 수 없다고 함. 
# #pk 체크하기전에 passwd 체크. 
# #추가로 관리자 퍼미션 체크 또는 이건 템플릿에 띄우기
# @user_passes_test(email_check)
# def my_view(request, pk):



@login_required
def room(request, room_pk):
    # 1. requesst.user has room permission?
    # 2. 

    #현재 로그인 되어있는 계정을 기준으로 퍼미션 체크를 한다.
    perimssion_codename = 'main.room_'+ str(room_pk) +'_view'
    
    #퍼미션을 가지고 있다면 정상적으로 페이지를 보여줌
    if request.user.has_perm(perimssion_codename):
        room = Room.objects.get(pk=room_pk)
        room_messages = reversed(room.messages.order_by('-timestamp')[:5])
        return render(request, 'chat/room.html', {
            'room_pk_json': mark_safe(json.dumps(room_pk)),
            'messages':room_messages,
            'room':room,#데이터 베이스를 통째로 넘겨줌
        })
    #퍼미션을 가지고 있지 않다면,
    else:
        messages.add_message(request, messages.ERROR, '권한이 없습니다.')
        return redirect('main:RoomList')

