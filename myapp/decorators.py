from django.http import HttpResponse
from django.shortcuts import render, redirect


def unauthenticate_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowerd_users(allowed_roles=[]):
    def dacorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page")
        return wrapper_func
    return dacorator


def admin_only(view_func):
    def wrapper_func(request, *args, **kawrgs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == "customer":
            return redirect('user')
        
        if group == "admin":
            return view_func(request, *args, **kawrgs)
    return wrapper_func

