# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Room, Message
from channels.db import database_sync_to_async
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #chat/routing.py 에 정의된 URL 파라미터에서 roomName을 얻음
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'room_'+ self.room_name +'_group'
        
        #현재 방주소로 된 Room 모델 객체를 불러온다.
        self.room_object = await self.get_room()
        print(self.room_object)


        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    @database_sync_to_async
    def get_room(self):
        return Room.objects.get(pk=self.room_name)

    @database_sync_to_async
    def save_message(self, username, message):
        m = Message(room=self.room_object, username=username, message=message)
        return m.save()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 웹소켓으로부터 메세지를 받아 처리하는 부분이다.
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        print("socket receive message: ", message)
        print("socket receive username: ", username)
        
        await self.save_message(username,message)

        # 아래에서는 그룹으로 메세지를 보내고 있다. chat_message 이벤트로 보냄.
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    # 위의 receive 메서드에서 그룹으로 메세지를 보내면 그 메세지를 받아 처리하는 부분이다.
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        timestamp = timezone.now()
        print("send all group log",username, message, timestamp)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'timestamp': timestamp.strftime('%Y년 %m월 %d일 %H:%M'),
        }))
