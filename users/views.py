from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout


def logout_page(request):
    logout(request)
    return redirect('main:index')

def login_page(request):
    return render(request, "login.html")
