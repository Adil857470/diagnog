from .views import *
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('signin/', signIn, name='signIn'),
    path('signup/', signUp, name='signUp'),
    path('activate/<uidb64>/<token>', activate, name="activate"),
    path('profile', userprofile, name="userprofile"),
    path('logout', logout, name="logout"),


]
