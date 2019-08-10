from django.shortcuts import render,redirect
from django.views import View
from .models import Posting
from django.contrib.auth.decorators import login_required
from .forms import CreateMain

from django.core.signing import Signer

# Create your views here.
@login_required
def main(request):
    print(request)
    postings=Posting.objects.all()
    return render(request, 'main/main.html', {'postings':postings, 'title': 'main page', 'body': 'this is main page'})

@login_required
def createMain(request):
    if request.method == 'POST':
        form = CreateMain(request.POST)
        if form.is_valid():#폼 형식이 맞으면
            form.save()
            return redirect('main:roomlist')#저장하고 main으로 보냄
        else:
            #맞지않으면 페이지에 계속 유지 시켜놓기
            return redirect('main:createMain')
    else:#post 요청이 아닐경우 form을 상속받아서, createMain.html로 전달
        form = CreateMain()
        return render(request,'main/createMain.html',{"form":form})
