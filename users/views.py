from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model, password_validation
from django.http import HttpResponseRedirect

User = get_user_model()


from . import models, forms

def logout_page(request):
    logout(request)
    return redirect('main:index')

def login_page(request):
    def next_redirect():
        return redirect(next_url if next_url else "main:index") # Redirect to next if have
    #
    next_url = request.GET.get("next")
    if request.user.is_authenticated:
        return next_redirect()
    register = request.POST.get('register')
    #
    if request.POST:
        if register:
            form = forms.RegisterForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                any_email = User.objects.filter(email=data['email'])
                if any_email.count() >= 1:
                    form.add_error('email', 'Пользователь с такой электронной почтой уже существует!')
                else:
                    try:
                        password_validation.validate_password(data['password'], form)
                    except forms.forms.ValidationError as error:
                        form.add_error('password', error)
                    else:
                        #
                        user = User(**data) # Pass data to new user
                        user.set_password(data['password'])
                        user.save()
                        #
                        return HttpResponseRedirect("?registered#login")

        else:
            # If Login mode
            form = forms.LoginForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user = authenticate(request, username=data['email'], password=data['password'])
                if user:
                    login(request, user)
                    #
                    return next_redirect()
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
