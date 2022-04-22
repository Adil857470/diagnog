from .views import *
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('sign-in/', signIn, name='signIn'),
    path('sign-up/', signUp, name='signUp'),


]
