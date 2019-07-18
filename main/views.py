from django.shortcuts import render
from django.views import View
from .models import Posting
from django.contrib.auth.decorators import login_required
# Create your views here.
def main(request):
    print(request)
    return render(request, 'main/main.html', {'title': 'main page', 'body': 'this is main page'})
@login_required
def seo(request):
    postings=Posting.objects.all()
    context={'postings':postings}
    return render(request,'main/seo.html',context)
