from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Posting(models.Model):
    group=models.CharField(max_length=30)
    roomname=models.CharField(max_length=100)
    author=models.ForeignKey(User,on_delete=True)
    logo=models.ImageField(blank=True)
    roompassword=models.CharField(max_length=30)
    roompasswordcheck=models.CharField(max_length=30)
    uploadfile=models.FileField(blank=True)

    def __str__(self):
        return '{} 개설자{}'.format(self.roomname,self.author)
