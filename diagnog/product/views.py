from django.shortcuts import render
from .models import *
from django.db.models import F
from datetime import datetime
from django.db.models import Avg, Max, Min, Sum
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
    return render(request, 'index/index.html', {"data": data, "trending_products": trending_product, 'best_selling_products': best_selling_product})
