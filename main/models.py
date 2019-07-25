from django.db import models

# Create your models here.
class Posting(models.Model):
    group=models.CharField(max_length=30)
    roomname=models.CharField(max_length=100)
    name=models.CharField(max_length=10)
    nowcount=models.IntegerField(default=1)
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()

    def __str__(self):
        return self.name
