from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings 

# Create your models here.
class Room(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)#작성자 
    group = models.CharField(max_length=30)#소속
    roomname = models.CharField(max_length=100)#main 에 보여질 방 이름
    password = models.CharField(max_length=30,null=True)
    uploadfile = models.FileField(blank=True, null=True, upload_to='pdf_uploads/%Y/%m/%d/')

    def __str__(self):
        return '{} 개설자{}'.format(self.roomname,self.author)
