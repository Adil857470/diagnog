from django.shortcuts import render
from .models import *
from django.db.models import F
from datetime import datetime
# Create your views here.


def index(request):
    data = Products.objects.all()
    for dat in data:
        delta = datetime.now().date() - dat.created_at
        days_gap = delta.days
        if days_gap <= 7:
            dat.new = True
        else:
            dat.new = False
    return render(request, 'index/index.html', {"data": data})
