from django.shortcuts import render,redirect
from django.views import View
from .models import Posting
from django.contrib.auth.decorators import login_required
from .forms import CreateMain
# Create your views here.
def main(request):
    print(request)
    return render(request, 'main/main.html', {'title': 'main page', 'body': 'this is main page'})
@login_required
def seo(request):
    postings=Posting.objects.all()
    context={'postings':postings}
    return render(request,'main/seo.html',context)

def createMain(request):
    if request.method == 'post':
        form = CreateMain(request.POST)

        if form.is_valid():
            form.save()
            return redirect('main')
        else:
            return redirect('seo')
    else:
        form = CreateMain()
        return render(request,'main/seo.html',{"form":form})
