from django.shortcuts import render, redirect
from product.models import Products
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

@login_required(login_url="/user/signin/")
def cart_add(request, id, quantity=1):
    cart = Cart(request)
    print("cart: ",cart)
    product = Products.objects.get(id=id)
    print("product: ",product)
    cart.add(product=product,quantity=quantity)
    print('+++++++++++++++++++++++++++')
    print(request.session.cart,'---------------------')
    return redirect('/')


@login_required(login_url="/user/signin/")
def item_clear(request, id):
    cart = Cart(request)
    product = Products.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/user/signin/")
def item_increment(request, id):
    cart = Cart(request)
    product = Products.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/user/signin/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Products.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/user/signin/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/user/signin/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')