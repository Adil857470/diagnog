from .views import *
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('signin/', signIn, name='signIn'),
    path('signup/', signUp, name='signUp'),


]
