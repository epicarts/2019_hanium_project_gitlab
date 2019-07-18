from django.db import models

# Create your models here.
class Posting(models.Model):
    group=models.CharField(max_length=30)
    roomname=models.CharField(max_length=100)
    name=models.CharField(max_length=10)
    nowcount=models.IntegerField(default=1)

    def __str__(self):
        return self.name
