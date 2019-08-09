from django import forms
from .models import Posting

class CreateMain(forms.ModelForm):
    class Meta:
        model=Posting
        fields = ['group', 'roomname', 'author','logo','roompassword','roompasswordcheck','uploadfile'] 
