from django import forms
from . import models

class LoginForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['email', 'password']

class RegisterForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['email', 'username', 'first_name', 'password']
    password2 = forms.CharField(max_length=70, required=True, widget=forms.PasswordInput, label="Повторите пароль")

class ChangePasswordForm(forms.Form):
    password = forms.CharField(max_length=70, required=True, widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(max_length=70, required=True, widget=forms.PasswordInput, label="Повторите Пароль")

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model  = models.User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
