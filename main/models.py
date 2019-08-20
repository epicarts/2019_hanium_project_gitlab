from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Room(models.Model):
    author = models.CharField(max_length=30)#작성자 
    group = models.CharField(max_length=30)#소속
    roomname = models.CharField(max_length=100)#main 에 보여질 방 이름
    password = models.CharField(max_length=30,null=True)
    uploadfile = models.FileField(blank=True)

    # class Meta:
    #     permissions = ( 
    #         ( "read_book", "Can read book" ),
    #     )

    def __str__(self):
        return '{} 개설자{}'.format(self.roomname,self.author)

#특정 사람: 처음에 방을 생성할 때 주인(user has perm model del)
#특정 사람: 처음에 패스워드를 뚫고 들어가는 사람.(user has per view 
#           또는 url 접근을 막을거임 @permission_required('deals.can_invest') ) 권한을 가진 사람만...
#특정 사람만 볼 수 있는 데이터 베이스(주인(del per있음.), )
# 방을 만들때 마다 그룹이 생김. 그룹만 방을 접근 할 수 있음.

