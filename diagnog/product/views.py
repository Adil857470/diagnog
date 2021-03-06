from audioop import add
from telnetlib import STATUS
from django.shortcuts import render, redirect
from .models import *
from django.db.models import F
from datetime import datetime
from django.db.models import Avg, Max, Min, Sum
# from .cart_view import *
from django.contrib.auth.decorators import login_required
# Create your views here.
import razorpay
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import *
from django.contrib.auth.models import User
message=None

def homePage(user):
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
    best_selling_product = Cart.objects.all().annotate(
        total_quantity=Avg('quantity')).order_by('-total_quantity')[0:8]
    added_by = False
    if user.id !=None:
        user = User.objects.filter(id=user.id).first()
        added_by = Profile.objects.filter(user=user).first()
        
    if added_by:
        cart = Cart.objects.filter(added_by=added_by,status='Pending')
        cart_count = cart.count()
    else:
        cart_count = 0
        cart = None
    return data,trending_product,best_selling_product,cart_count,cart

def index(request):
    homepage_data = homePage(user = request.user)
    data = homepage_data[0]
    trending_product = homepage_data[1]
    best_selling_product = homepage_data[2]
    cart_count = homepage_data[3]
    cart = homepage_data[4]
    return render(request, 'index/index.html', {"data": data, "trending_products": trending_product, 'best_selling_products': best_selling_product,'cart_count':cart_count,"cart":cart})


def productDescription(request, id=None):
    data = Products.objects.filter(id=id).first()
    image = ProductImages.objects.filter(name=data.id).first()
    image_url = 'https://diagnog-media.s3.us-east-1.amazonaws.com/' + \
        str(image.image)
    data.image = image_url
    added_by = False
    if request.user.id !=None:
        user = User.objects.filter(id=request.user.id).first()
        added_by = Profile.objects.filter(user=user).first()
    if added_by:
        cart = Cart.objects.filter(added_by=added_by,status='Pending')
        cart_count = cart.count()
    else:
        cart_count = 0
        cart = None
    return render(request, 'index/description.html', {"data": data,"cart_count":cart_count,"cart":cart})


@login_required(login_url="/user/signin/")
def cart_add(request, id, qty = 1):
    product = Products.objects.get(id=id)
    added_by = False
    if request.user.id !=None:
        user = User.objects.filter(id=request.user.id).first()
        print(user)
        added_by = Profile.objects.filter(user=user).first()
        print("_____________________________IF_____________________________",added_by)
    print(added_by,'-------------------------',request.user.id)
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

@login_required(login_url="/user/signin/")
def remove_cart(request,id):
    added_by = False
    if request.user.id !=None:
        user = User.objects.filter(id=request.user.id).first()
        added_by = Profile.objects.filter(user=user).first()
    Cart.objects.filter(id=id,added_by=added_by).delete()
    return JsonResponse({'status': 'ok'})
    
    

#_______________________________PAYMENT_____RAZOR____PAY________________________________
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def razor_pay_form(request):
    added_by = False
    if request.user.id !=None:
        user = User.objects.filter(id=request.user.id).first()
        added_by = Profile.objects.filter(user=user).first()
    if added_by:
        carts = Cart.objects.filter(added_by=added_by,status='Pending')
        total = 0
        for cart in carts:
            total = total+(int(cart.quantity)*float(cart.product.price))
        data = {"total":total,"username":added_by.user}
    else:
        data = {"message":"Please add somehting to cart!"}
    return render(request,'index/razor_pay.html', data)
    
@login_required(login_url="/user/signin/")
def order_payment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        razorpay_order = razorpay_client.order.create(
            {"amount": float(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order_id = '#'
        order_id = order_id + str(request.user.id) + str(datetime.now().strftime("%Y%m%d%H%M%S"))
        user = User.objects.filter(id=request.user.id).first()
        added_by = Profile.objects.filter(user=user).first()
        cart = Cart.objects.filter(added_by=added_by,status='Pending')
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=razorpay_order['id'],cart=cart.first(),payment_id=razorpay_order['id'],order_by=added_by
        )
        order.save()
        # cart.update(status='Purchased') # for testing purpose on production uncomment this line 
        context = {}
        context['razorpay_order_id'] = razorpay_order['id']
        context['razorpay_key'] = settings.RAZORPAY_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = "INR"
        context['callback_url'] = 'callback/'
        context['order'] = order
        return render(
            request,
            "index/payment.html",
            context=context,
        )
    return render(request, "index/payment.html")

@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)
    homepage_data = homePage(user = request.user)
    data = homepage_data[0]
    trending_product = homepage_data[1]
    best_selling_product = homepage_data[2]
    cart_count = homepage_data[3]
    cart = homepage_data[4]
    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, 'index/index.html', {"data": data, "trending_products": trending_product, 'best_selling_products': best_selling_product,'cart_count':cart_count,"cart":cart,"status": "THANKS YOUR PAYMENT HAS BEEN RECEIVED"})
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, 'index/index.html', {"data": data, "trending_products": trending_product, 'best_selling_products': best_selling_product,'cart_count':cart_count,"cart":cart,"status": "SORRY, YOUR PAYMENT HAS BEEN FAILED"})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, 'index/index.html', {"data": data, "trending_products": trending_product, 'best_selling_products': best_selling_product,'cart_count':cart_count,"cart":cart,"status": "SORRY, YOUR PAYMENT HAS BEEN FAILED"})

