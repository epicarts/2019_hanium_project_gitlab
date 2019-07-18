from django.shortcuts import render
from django.views import View

# Create your views here.
def main(request):
    print(request)
    return render(request, 'main/main.html', {'title': 'main page', 'body': 'this is main page'})
