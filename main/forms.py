from django import forms
from .models import Room

class CreateMain(forms.ModelForm):
    #일반 폼
    confirm_password = forms.CharField(label = '비밀번호 확인', widget=forms.PasswordInput())

    #모델 폼
    class Meta:
        model=Room
        fields = ['group', 'roomname','password','confirm_password','uploadfile'] 
        widgets = {
            'password' : forms.PasswordInput(),
        }