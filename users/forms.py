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

class ChangePasswordForm(forms.Form):
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput, label="Повторите Пароль")
