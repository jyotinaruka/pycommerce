from django.shortcuts import render, HttpResponse, redirect
from pycommerce_app.models import Customer, Product, Category, Order, ShoppingCart, ShoppingCartItem
from django.contrib import messages
import bcrypt
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users


def index(request):
    customer = None
    if "customer_id" in request.session:
        customer_id = request.session['customer_id']
        customer = Customer.objects.get(id=customer_id)

    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        "customer": customer,
        "categories": categories,
        "products": products
    }
    return render(request, 'index.html', context)


def category(request, id):
    customer = None
    if "customer_id" in request.session:
        customer_id = request.session['customer_id']
        customer = Customer.objects.get(id=customer_id)

    categories = Category.objects.all()
    products = Product.objects.filter(categories__id=id)
    context = {
        "customer": customer,
        "categories": categories,
        "products": products
    }
    return render(request, 'index.html', context)


def product_detail(request, id):
    customer = None
    if "customer_id" in request.session:
        customer_id = request.session['customer_id']
        customer = Customer.objects.get(id=customer_id)

    product = Product.objects.get(id=id)
    context = {
        "customer": customer,
        "product": product
    }
    return render(request, 'product.html', context)


def cart(request):
    if "customer_id" not in request.session:
        return redirect("/register_login")

    customer_id = request.session['customer_id']
    customer = Customer.objects.get(id=customer_id)
    carts = ShoppingCart.objects.filter(customer__id=customer_id)
    if carts:
        cart = carts[0]
    else:
        cart = ShoppingCart()
        cart.customer = customer
        cart.save()

    total = 0
    for item in cart.items.all():
        total += item.quantity * item.product.price
    context = {
        "customer": customer,
        "cart": cart,
        "total": total
    }
    return render(request, 'cart.html', context)


def cart_shipping(request):
    # TODO create orders
    return redirect('/success')


def thank_you_page(request):
    customer = None
    if "customer_id" in request.session:
        customer_id = request.session['customer_id']
        customer = Customer.objects.get(id=customer_id)

    context = {
        "customer": customer
    }
    return render(request, 'thankyou.html', context)


def add_cart(request):
    if "customer_id" not in request.session:
        return redirect("/register_login")

    customer_id = request.session['customer_id']
    customer = Customer.objects.get(id=customer_id)
    cart = ShoppingCart.objects.filter(customer__id=customer_id).first()
    if cart:
        pass
    else:
        cart = ShoppingCart()
        cart.customer = customer
        cart.save()

    quantity = int(request.POST["quantity"])
    if quantity < 1 or quantity > 10:
        return redirect("/")

    product_id = request.POST["product_id"]
    product = Product.objects.get(id=product_id)

    cart_item = ShoppingCartItem.objects.filter(
        cart__id=cart.id, product__id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        cart_item = ShoppingCartItem.objects.create(
            cart=cart, quantity=quantity, product=product)

    return redirect("/cart")


def cart_update(request):
    if "customer_id" not in request.session:
        return redirect("/register_login")

    id = request.POST["id"]
    quantity = int(request.POST["quantity"])
    db_cart_item = ShoppingCartItem.objects.get(id=id)
    if quantity < 1:
        db_cart_item.delete()
    else:
        db_cart_item.quantity = quantity
        db_cart_item.save()
    return redirect("/cart")


def register_login(request):
    return render(request, 'register_login.html')


def register(request):
    errors = Customer.objects.register_validator(request.POST)
    if len(errors) > 0:
        for msg in errors:
            messages.error(request, errors[msg])
        return redirect('/register_login')

    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_customer = Customer.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=pw_hash,
    )

    request.session['customer_id'] = new_customer.id

    return redirect('/dashboard/products')


def login(request):
    errors = Customer.objects.login_validator(request.POST)
    if len(errors) > 0:
        for msg in errors:
            messages.error(request, errors[msg])
        return redirect('/register_login?error=BadCredentials')

    all_customers = Customer.objects.filter(email=request.POST['email'])
    if len(all_customers) > 0:
        customer = all_customers[0]
        if bcrypt.checkpw(request.POST['password'].encode(), customer.password.encode()):
            request.session['customer_id'] = customer.id
            return redirect('/dashboard/products')
    return redirect('/register_login?error=BadUser')


def logout(request):
    request.session.clear()
    return redirect('/')

#####################################
# Only Admins Can Access These Pages


@login_required(login_url='/')
# @allowed_users(allowed_roles=['admin'])
def dashboard(request):
    customers = Customer.objects.all()
    products = Product.objects.all()
    orders = Order.objects.all()
    shopped_items = ShoppingCart.objects.all()

    context = {
        'customers': customers,
        'products': products,
        'orders': orders,
        'shopped_items': shopped_items
    }
    return render(request, 'dashboard/index.html', context)


@login_required(login_url='/')
def all_products(request):
    all_products = Product.objects.all()
    context = {
        "products": all_products
    }

    return render(request, 'dashboard/products.html', context)


@login_required(login_url='/')
def showproduct(request, product_id):
    this_product = Product.objects.get(id=product_id)
    categories = Category.objects.all()
    context = {
        "product": this_product,
        "categories": categories
    }

    return render(request, 'dashboard/singleproduct.html', context)


@login_required(login_url='/')
def editproduct(request):
    image_url = "placeholder"
    if len(request.POST['image_url']) > 0:
        image_url = request.POST['image_url']

    this_product = Product.objects.get(id=request.POST['product_id'])
    this_product.title = request.POST['title']
    this_product.desc = request.POST['desc']
    this_product.image_url = image_url
    this_product.save()

    if len(request.POST['new_category']) > 0:
        new_category = Category.objects.create(
            name=request.POST['new_category'])
        this_product.categories.add(new_category)

    category_id = int(request.POST['category'])
    category = Category.objects.get(id=category_id)
    this_product.categories.add(category)
    this_product.save()

    return redirect('dashboard/products')


@login_required(login_url='/')
def newproduct(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'dashboard/newproduct.html', context)


@login_required(login_url='/')
def addnewproduct(request):
    image_url = "placeholder"
    if len(request.POST['image_url']) > 0:
        image_url = request.POST['image_url']

    this_product = Product.objects.create(
        title=request.POST['title'],
        desc=request.POST['desc'],
        price=request.POST['price'],
        inventory=request.POST['inventory'],
        quantity_sold=request.POST['quantity_sold'],
        image_url=image_url
    )

    if len(request.POST['new_category']) > 0:
        new_category = Category.objects.create(
            name=request.POST['new_category'])
        this_product.categories.add(new_category)

    category_id = int(request.POST['category'])
    category = Category.objects.get(id=category_id)
    this_product.categories.add(category)
    this_product.save()

    return redirect('dashboard/products')


@login_required(login_url='/')
def deleteproduct(request):
    this_product = Product.objects.get(id=request.POST['product_id'])
    this_product.delete()

    return redirect('dashboard/products')
