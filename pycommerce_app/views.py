from django.shortcuts import render, HttpResponse, redirect
from pycommerce_app.models import Customer, Product, Category, Order
from django.contrib import messages
import bcrypt
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users

def index(request):
    category = Category.objects.first()
    return redirect(f"/category/{category.id}")


def category(request, id):
    categories = Category.objects.all()
    products = Product.objects.filter(Categories__id=id)
    context = {
        "categories": categories,
        "products": products
    }
    return render(request, 'index.html', context)

def product_detail(request, id):
    product = Product.objects.get(id=id)
    context = {
        'product': product
    }
    return render(request, 'product.html', context)


def cart(request):

    return render(request, 'cart.html')


def cart_shipping(request):

    return redirect('/success')


def thank_you_page(request):
    return render(request, 'thankyou.html')

# admin pages

def register_login(request):
    return render(request, 'register_login.html')

<<<<<<< HEAD
def register(request):
    errors = Customer.objects.register_validator(request.POST)
    if len(errors) > 0:
        for msg in errors:
            messages.error(request, errors[msg])
        return redirect('/')

    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_customer = Customer.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
        password = pw_hash,
    )
    
    request.session['customer_id'] = new_customer.id

    return redirect('/dashboard/products')

def login(request):
    errors = Customer.objects.login_validator(request.POST)
    if len(errors) > 0:
        for msg in errors:
            messages.error(request, errors[msg])
        return redirect('/')

    all_customers = Customer.objects.filter(email = request.POST['email'])
    if len(all_customers) > 0:
        customer = all_customers[0]
        if bcrypt.checkpw(request.POST['password'].encode(), customer.password.encode()):
            request.session['customer_id'] = customer.id
            return redirect('/dashboard/products')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/register_login')

#####################################
# Only Admins Can Access These Pages
@login_required(login_url='/')
# @allowed_users(allowed_roles=['admin'])
def dashboard(request):
    customers = Customer.objects.all()
    products = Product.objects.all()
    context = {
        'customers': customers,
        'products' : products
    }
    return render(request, 'dashboard/index.html', context)

@login_required(login_url='/')
=======

>>>>>>> 613143579ae889d864ba337eb8d3022bddc59f3d
def all_products(request):
    all_products = Product.objects.all()
    context = {
        "products": all_products
    }

    return render(request, 'dashboard/products.html', context)

<<<<<<< HEAD
@login_required(login_url='/')
=======

>>>>>>> 613143579ae889d864ba337eb8d3022bddc59f3d
def showproduct(request, product_id):
    this_product = Product.objects.get(id=product_id)
    categories = Category.objects.all()
    context = {
        "product": this_product,
        "categories": categories
    }

    return render(request, 'dashboard/singleproduct.html', context)

<<<<<<< HEAD
@login_required(login_url='/')
=======

>>>>>>> 613143579ae889d864ba337eb8d3022bddc59f3d
def editproduct(request):
    this_product = Product.objects.get(id=request.POST['product_id'])
    this_product.title = request.POST['title']
    this_product.desc = request.POST['desc']
<<<<<<< HEAD
=======
    # this_product.categories.name = request.POST['category']
    # new_category = request.POST['new_category']
    this_product.image_url = request.POST['image_url']
>>>>>>> 613143579ae889d864ba337eb8d3022bddc59f3d
    this_product.save()

    Category.objects.create(name= request.POST['new_category'])
    new_category = Category.objects.last()
    this_product.categories.add(new_category)

    categories = request.POST.getlist('category')
    for category in categories:
        this_product.categories.add(category)

    return redirect('dashboard/products')

<<<<<<< HEAD
@login_required(login_url='/')
=======

>>>>>>> 613143579ae889d864ba337eb8d3022bddc59f3d
def newproduct(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories
    }
    return render(request, 'dashboard/newproduct.html', context)

<<<<<<< HEAD
@login_required(login_url='/')
=======

>>>>>>> 613143579ae889d864ba337eb8d3022bddc59f3d
def addnewproduct(request):

    Product.objects.create(
        title=request.POST['title'],
        desc=request.POST['desc'],
        price=request.POST['price'],
        inventory=request.POST['inventory'],
        quantity_sold=request.POST['quantity_sold'],
        image_url="placeholder"
    )

    return redirect('dashboard/products')

<<<<<<< HEAD
@login_required(login_url='/')
=======

>>>>>>> 613143579ae889d864ba337eb8d3022bddc59f3d
def deleteproduct(request):
    this_product = Product.objects.get(id=request.POST['product_id'])
    this_product.delete()

    return redirect('dashboard/products')
