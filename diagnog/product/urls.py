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
    # path('payment/', homepage, name='index'),
    # path('paymenthandler/', paymenthandler, name='paymenthandler'),
    
    
#     path('cart/item_clear/<int:id>/', item_clear, name='item_clear'),
#     path('cart/item_increment/<int:id>/',
#          item_increment, name='item_increment'),
#     path('cart/item_decrement/<int:id>/',
#          item_decrement, name='item_decrement'),
#     path('cart/cart_clear/', cart_clear, name='cart_clear'),
#     path('cart/cart-detail/',cart_detail,name='cart_detail'),


]
