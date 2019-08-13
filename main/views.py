from django.shortcuts import render,redirect
from django.views import View
from .models import Room
from django.contrib.auth.decorators import login_required
from .forms import CreateMain
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

from django.core.signing import Signer

# Create your views here.
@login_required
def main(request):
    RoomList=Room.objects.all()
    return render(request, 'main/main.html', {'RoomList':RoomList, 'title': 'main page', 'body': 'this is main page'})



# def deleteRoom(request, room_id):
#     if room.owner == requset.suer:
#         room.delete () 
#         return 
#     return "권한이 없ㅅ브니다" 

    

@login_required
def createMain(request):
    print(request.user)
    key = Room.objects.last()

    # 다른 앱에 있는 모델을 가져 올 수도 있음.
    '''
    content_type = ContentType.objects.get(app_label='myapp', model='BlogPost')
    '''

    # auth | 사용자 | Can access RoomList 이런식으로 추가됨
    # 즉, auth 앱에 사용자라는 모델 전부에 코드네임 can_accessasad 이름으로 권한이 추가됨. 이걸 어떻게 쓸지는 내 마음.
    # ct = ContentType.objects.get_for_model(Room) # 모델을 가져와서 유저에 매칭 ??? 
    # permission = Permission.objects.get_or_create(codename='can_acces4sac3sad', name='Can access RoomList', content_type=ct)
    # print("get_or_create",permission[0])
    # permission = Permission.objects.get(codename='can_acces4sac3sad')
    # print("get",permission)

    '''
    content_type = ContentType.objects.get(app_label='myapp', model='BlogPost')
    permission = Permission.objects.create(codename='can_publish',
                                        name='Can Publish Posts',
                                        content_type=content_type)
    user = User.objects.get(username='duke_nukem')
    group = Group.objects.get(name='wizard')
    group.permissions.add(permission)
    user.groups.add(group)
    '''
    '''

    #새로운 그룹 정보를 가져온 뒤
    group = Group.objects.get(name='new_group')
    print("new_group",new_group,"///group",group)

    

    #해당 그룹에 퍼미션을 추가 시킨다. 퍼미션은 위에서 만든 새로운 퍼미션
    # group.permissions.add(permission)

    #유저는 유저 이름을 가져오는것으로 유저를 불러올 수 있다.
    user = User.objects.get(username=request.user) # username= request.user
    print("request.user",request.user,"///user",user)

    #user는 그룹에 가입을 시킴으로 써 퍼미션을 가질 수 있다.
    request.user.groups.add(new_group)
    request.user.groups.add(group)
    '''

    if request.method == 'POST':
        form = CreateMain(request.POST)
        if form.is_valid():#폼 형식이 맞으면
            #cleaned_data는 사용자가 입력한 데이터를 뜻한다.
            if form.cleaned_data['password']  == form.cleaned_data['confirm_password']:
                post = form.save(commit=False) # 함수 호출 지연
                post.author = request.user # 유저 id 필드는 유저로 부터 입력 받지 않고 프로그램으로 채워 넣는다
                post.save()

                print(post.pk)
                '''
                그룹 및 권한 추가
                그룹: room_{pk}_group
                권한: room_{pk}_view  / room_{pk}_delete
                '''
                groupname = 'room_'+ str(post.pk) +'_group'

                #그룹이 없다면 생성하거나 가져옴. 그룹 이름은 방을 생성할 때 방 그룹은 id room_id 
                new_group, created = Group.objects.get_or_create(name=groupname)
                #그룹에 권한(permission 생성 및 추가)
                perimssion_codename = 'room_'+ str(post.pk) +'_view'
                perimssion_name = 'Can view Room ' + str(post.pk) 
                content_type = ContentType.objects.get(app_label='main', model='Room')
                permission = Permission.objects.create(codename=perimssion_codename, name=perimssion_name, content_type=content_type)
                new_group.permissions.add(permission)#그룹에 권한 추가
                request.user.groups.add(new_group)#그룹에 개인 추가


                # Code to add permission to group 
                # room 모델을 삭제할 수 있는 permission을 만듬
                perimssion_codename = 'room_'+ str(post.pk) +'_delete'
                perimssion_name = 'Can delete Room ' + str(post.pk) 
                content_type = ContentType.objects.get(app_label='main', model='Room')
                permission = Permission.objects.create(codename=perimssion_codename, name=perimssion_name, content_type=content_type)
                request.user.user_permissions.add(permission)#방 생성한 사람에게 권한을 줌

                #redirect('/detail/'+str(cat.pk)) 저장하고 만들어진 페이지로
                return redirect('main:RoomList')#저장하고 main으로 

            else:##password와 password_check가 다를 것을 대비하여 error를 지정해준다.
                return redirect('main:createMain')

            
            

        else:#맞지않으면 페이지에 계속 유지 시켜놓기
            return redirect('main:createMain')
    else:#post 요청이 아닐경우 form을 상속받아서, createMain.html로 전달
        form = CreateMain()
        return render(request,'main/createMain.html',{"form":form})
