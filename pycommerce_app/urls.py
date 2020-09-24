from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register_login', views.register_login),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('dashboard/products', views.all_products),
    path('dashboard/products/<int:product_id>', views.showproduct),
    path('editproduct', views.editproduct),
    path('dashboard/products/newproduct', views.newproduct),
    path('addnewproduct', views.addnewproduct),
    path('deleteproduct', views.deleteproduct),
    path('category/<int:id>', views.category),
    path('product/<int:id>', views.product_detail),
    path('cart', views.cart),
    path('cart/shipping', views.cart_shipping),
    path('cart/add', views.add_cart),
    path('cart/update', views.cart_update),
    path('success', views.thank_you_page),

]
