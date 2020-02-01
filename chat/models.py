from django.db import models
from django.utils import timezone
from main.models import Room

# main.models.Room 을 외래키로 가져옴
class Message(models.Model):
    
    #바라보는 값이 삭제 되면 같이 삭제됨.
    room = models.ForeignKey(Room,on_delete=models.CASCADE, related_name='messages')
    username = models.TextField()
    message = models.TextField(max_length=3000)
    timestamp = models.DateTimeField(auto_now_add=True,db_index=True)

    def formated_timestamp(self):
        return self.timestamp.strftime('%H:%M')

    
    # def __unicode__(self):
    #     return '[{timestamp}] {username}:{message}'.format(**self.as_dict())

    # def as_dict(self):
    #     return {'username':self.username, 'message':self.message, 'timestamp':self.timestamp}