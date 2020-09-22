from django.shortcuts import render, HttpResponse, redirect


def index(request):
    return render(request, 'index.html')


def product_detail(request, id):
    return render(request, 'product.html')


def register_login(request):
    return render(request, 'register_login.html')
