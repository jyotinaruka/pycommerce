from django.shortcuts import render, HttpResponse, redirect
from pycommerce_app.models import User, Product, Category, Order


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


def all_products(request):
    all_products = Product.objects.all()
    context = {
        "products": all_products
    }

    return render(request, 'dashboard/products.html', context)


def showproduct(request, product_id):
    this_product = Product.objects.get(id=product_id)
    categories = Category.objects.all()
    context = {
        "product": this_product,
        "categories": categories
    }

    return render(request, 'dashboard/singleproduct.html', context)


def editproduct(request):
    this_product = Product.objects.get(id=request.POST['product_id'])
    this_product.title = request.POST['title']
    this_product.desc = request.POST['desc']
    # this_product.categories.name = request.POST['category']
    # new_category = request.POST['new_category']
    this_product.image_url = request.POST['image_url']
    this_product.save()
    return redirect('dashboard/products')


def newproduct(request):
    return render(request, 'dashboard/newproduct.html')


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


def deleteproduct(request):
    this_product = Product.objects.get(id=request.POST['product_id'])
    this_product.delete()

    return redirect('dashboard/products')
