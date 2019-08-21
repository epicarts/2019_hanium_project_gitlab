from django import forms

class RegistrationFrom(forms.Form):
    username = forms.CharField(label="사용자 이름", max_length=30)
    password1 = forms.CharField(label="비밀번호", widget=forms.PasswordInput())
    password2 = forms.CharField(label="비밀번호 확인", widget=forms.PasswordInput())


class PasswordChangeFrom(forms.Form):
    current_password = forms.CharField(label = '현재 비밀번호', widget=forms.PasswordInput())
    new_password = forms.CharField(label = '새 비밀번호', widget=forms.PasswordInput())
    confirm_new_password = forms.CharField(label = '새 비밀번호 확인', widget=forms.PasswordInput())
