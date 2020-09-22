from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
<<<<<<< HEAD
    path('register_login', views.register_login),
    path('dashboard/products', views.all_products),
    path('dashboard/products/<int:product_id>', views.showproduct),
    path('editproduct', views.editproduct),
    path('dashboard/products/newproduct', views.newproduct),
    path('addnewproduct', views.addnewproduct),
    path('deleteproduct', views.deleteproduct),

=======
    #path('category/<int:id>', views.category),
    path('product/<int:id>', views.product_detail),
    path('register_login', views.register_login)
>>>>>>> ca13bc2dcc4f749401e55b03b8179d0fbd40b5aa
]
