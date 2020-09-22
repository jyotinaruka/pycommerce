from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    #path('category/<int:id>', views.category),
    path('product/<int:id>', views.product_detail),
    path('register_login', views.register_login)
]
