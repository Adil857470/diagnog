from audioop import add
from django.shortcuts import render, redirect
from .models import *
from django.db.models import F
from datetime import datetime
from django.db.models import Avg, Max, Min, Sum
# from .cart_view import *
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    data = Products.objects.all()[0:8]
    for dat in data:
        delta = datetime.now().date() - dat.created_at
        days_gap = delta.days
        if days_gap <= 7:
            dat.new = True
        else:
            dat.new = False
    trending_product = ProductRating.objects.all().annotate(
        avg_rating=Avg('rating')).filter(avg_rating__gte=3.5)[0:4]
    best_selling_product = Orders.objects.all().annotate(
        total_quantity=Avg('quantity')).order_by('-total_quantity')[0:8]
    
    added_by = Profile.objects.filter(id=request.user.id).first()
    cart = Cart.objects.filter(added_by=added_by).count()
    return render(request, 'index/index.html', {"data": data, "trending_products": trending_product, 'best_selling_products': best_selling_product,'cart':cart})


def productDescription(request, id=None):
    data = Products.objects.filter(id=id).first()
    image = ProductImages.objects.filter(name=data.id).first()
    image_url = 'https://diagnog-media.s3.us-east-1.amazonaws.com/' + \
        str(image.image)
    data.image = image_url
    added_by = Profile.objects.filter(id=request.user.id).first()
    cart = Cart.objects.filter(added_by=added_by).count()
    return render(request, 'index/description.html', {"data": data,"cart":cart})


@login_required(login_url="/user/signin/")
def cart_add(request, id, qty = 1):
    product = Products.objects.get(id=id)
    added_by = Profile.objects.filter(id=request.user.id).first()
    cart = Cart.objects.filter(product=product,added_by=added_by)
    if cart.exists():
        cart = cart.first()
    else:    
        cart = Cart()    
    cart.product = product
    cart.added_by = added_by
    cart.quantity = qty
    cart.save()
    return redirect("index")