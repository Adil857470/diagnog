from .views import *
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('product-description/<int:id>',
         productDescription, name='productDescription'),
    
    
    
    #________________________________________________________________________________________
    path('cart_add/<int:id>/<str:qty>', cart_add, name='cart_add'),
    path('payment_form/', razor_pay_form, name='payment_form'),
    path('payment/', order_payment, name='payment'),
    path("payment/callback/", callback, name="callback"),
    path('remove_cart/<int:id>', remove_cart, name='remove_cart'),

]
