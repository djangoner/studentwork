import logging
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout, get_user_model, password_validation
from django.http import HttpResponseRedirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from . import models, forms
from .tokens import account_activation_token, password_reset_generator

User = get_user_model()



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
                elif data['password'] != data['password2']:
                    form.add_error('password', 'Пароли не совпадают!')
                else:
                    try:
                        password_validation.validate_password(data['password'], form)
                    except forms.forms.ValidationError as error:
                        form.add_error('password', error)
                    else:
                        data.pop('password2')
                        #
                        user = User(**data) # Pass data to new user
                        user.set_password(data['password'])
                        user.is_active       = True
                        user.email_confirmed = False
                        user.save()
                        request.session['email'] = user.email
                        #
                        return redirect("users:email_confirm")
                        # return HttpResponseRedirect("?registered#login")

        else:
            # If Login mode
            form = forms.LoginForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user = authenticate(request, username=data['email'], password=data['password'])
                if user:
                    if not user.email_confirmed:
                        request.session["email"] = data['email']
                        messages.add_message(request, messages.WARNING, "Ваш Email не подтвержден. <a href='{}'>Страница подтверждения Email</a>".format(reverse("users:email_confirm")))
                    else:
                        login(request, user)
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
                messages.add_message(request, messages.SUCCESS, "Пароль успешно изменен. Вам требуется войти в аккаунт с новым паролем.")
                return redirect('main:cabinet')
                # context['changed'] = True
    else:
        form = forms.ChangePasswordForm()

    context['form'] = form
    return render(request, "change_password.html", context=context)


def email_confirm(request):
    email = request.session.get("email")
    #
    try:
        user = models.User.objects.get(email=email)
    except models.User.DoesNotExist:
        user = None
    #
    if user and (not user.email_confirmed and "resend" in request.GET):
        try:
            user.send_confirmation_email()
        except:
            messages.add_message(request, messages.ERROR, "Не удалось отправить письмо, проверьте правильно ли указан Email адрес")
        else:
            messages.add_message(request, messages.INFO, "Письмо успешно отправлено")
        return HttpResponseRedirect("?")
    if request.method == "POST":
        form = forms.EmailChangeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_email = data["email"]
            #
            if models.User.objects.filter(email=new_email).count() > 0:
                messages.add_message(request, messages.WARNING, "Этот Email уже используется")
            else:
                user.email = new_email
                user.save()
                request.session["email"] = new_email
                #
                return HttpResponseRedirect("?resend")
        else:
            messages.add_message(request, messages.WARNING, "Неверный Email адрес")
    else:
        form = forms.EmailChangeForm()
    #
    context = {
        "email": email,
        "user": user,
        "form": form,
    }
    return render(request, "email_confirm.html", context=context)


def activate(request, uidb64, token):
    activated = False

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = models.User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    already_activated = user.email_confirmed if user else False
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        activated = True
        # return redirect('home')
    context = {
        "activated": activated,
        "already_activated": already_activated
    }
    return render(request, "account_activated.html", context=context)


def password_reset_page(request):
    if request.POST:
        form = forms.EmailChangeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email = data['email']
            #
            matching_users = models.User.objects.filter(email=email)
            if matching_users.count() < 1:
                messages.add_message(request, messages.WARNING, "Указанный Email не привязан к пользователю")
            else:
                try:
                    matching_users.first().send_password_reset_email()
                except Exception as err:
                    logging.exception("Password reset email err", exc_info=err)
                    messages.add_message(request, messages.WARNING, "Не удалось отправить письмо на указанный Email")
                else:
                    messages.add_message(request, messages.SUCCESS, "Письмо успешно отправлено, проверьте ваш Email")
        else:
            messages.add_message(request, messages.WARNING, "Не валидный Email адресс")
    return render(request, "password_reset_page.html")


def password_reset_form(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = models.User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    ##
    if not user:
        messages.add_message(request, messages.INFO, 'Ссылка сброса пароля была недействительна')
        return redirect('users:main')
    if request.POST:
        form = forms.ChangePasswordForm(request.POST)
        if form.is_valid() and user:
            data = form.cleaned_data
            if data["password"] != data["password2"]:
                form.add_error('password', forms.forms.ValidationError('Пароли не совпадают'))
            else:
                user.set_password(data["password"])
                user.save()
                messages.add_message(request, messages.SUCCESS, "Пароль успешно изменен")
                return redirect("users:login")
    else:
        form = forms.ChangePasswordForm()
    context = {
        'user': user,
        'form': form,
    }
    return render(request, "change_password.html", context=context)