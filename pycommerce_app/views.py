from django.shortcuts import render, HttpResponse, redirect


def index(request):
    return render(request, 'index.html')

def register_login(request):
    return render(request, 'register_login.html')
