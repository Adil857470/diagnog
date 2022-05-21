from pyexpat import model
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, null=True)
    flat_no = models.CharField(max_length=50, null=True)
    address_line_1 = models.CharField(max_length=200, null=True)
    address_line_2 = models.CharField(max_length=200, null=True)
    land_mark = models.CharField(max_length=100, null=True)
    pin_code = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.username
