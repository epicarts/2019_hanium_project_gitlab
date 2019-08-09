# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
import json
from .models import Room
from django.utils import timezone


def index(request):
    return render(request, 'chat/index.html', {})

# @login_required
# def new_room(request, room_name):
#     return redirect(room,label='새로 만들 방 이름을 라벨로...')

@login_required
def room(request, room_name):
    #room 이 있다면 생성
    room, created = Room.objects.get_or_create(label=room_name)
    messages = reversed(room.messages.order_by('-timestamp')[:5])
    #print(messages)
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'messages':messages,
        'room':room,#데이터 베이스를 통째로 넘겨줌
    })
