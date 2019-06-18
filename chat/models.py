from django.db import models
from django.utils import timezone

class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)

    def __unicode__(self):
        return self.label

class Message(models.Model):
    
    #바라보는 값이 삭제 되면 같이 삭제됨.
    room = models.ForeignKey(Room,on_delete=models.CASCADE, related_name='messages')
    username = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now,db_index=True)

    def __unicode__(self):
        return '[{timestamp}] {username}:{message}'.format(**self.as_dict())

    def as_dict(self):
        return {'username':self.username, 'message':self.message, 'timestamp':self.timestamp}
