from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from . import models, forms

def logout_page(request):
    logout(request)
    return redirect('main:index')

def login_page(request):
    if request.POST:
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['email'], password=data['password'])
            if user:
                login(request, user)
                #
                next_url = request.GET.get("next")
                return redirect(next_url if next_url else "main:index")
            else:
                form.add_error('email', forms.forms.ValidationError('Неверное имя пользователя или пароль'))
    else:
        form = forms.LoginForm()

    context = {
        'form': form,
    }
    return render(request, "login.html", context = context)

def change_password(request):
    context = {}
    if request.POST:
        form = forms.ChangePasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data["password"] != data["password2"]:
                form.add_error('password', forms.forms.ValidationError('Пароли не совпадают'))
            else:
                request.user.set_password(data["password"])
                request.user.save()
                context['changed'] = True
    else:
        form = forms.ChangePasswordForm()

    context['form'] = form
    return render(request, "change_password.html", context=context)
