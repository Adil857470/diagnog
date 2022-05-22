from .views import *
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('product-description/<int:id>',
         productDescription, name='productDescription'),


]
