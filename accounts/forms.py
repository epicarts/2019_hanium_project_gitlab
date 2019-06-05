from django import forms

class RegistrationFrom(forms.Form):
    username = forms.CharField(label="사용자 이름", max_length=30)
    password2 = forms.CharField(label="비밀번호 확인", widget=forms.PasswordInput())
    password1 = forms.CharField(label="비밀번호", widget=forms.PasswordInput())
