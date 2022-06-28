from pyexpat import model
from django.db import models
from user.models import Profile

# Create your models here.
from datetime import datetime
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus


class Products(models.Model):
    ''' Model for Products '''
    name = models.CharField(max_length=255, null=True)
    base_price = models.CharField(max_length=100, null=True)
    price = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def getImage(self):
        image = ProductImages.objects.filter(name=self.id).first()
        image_url = 'https://diagnog-media.s3.us-east-1.amazonaws.com/' + \
            str(image.image)
        return image_url

    def getRatings(self):
        all_rating = ProductRating.objects.filter(
            name=self.id).aggregate(Avg('rating'))
        return all_rating


class ProductImages(models.Model):
    ''' Model for Products Images'''
    name = models.ForeignKey(Products, on_delete=models.CASCADE)
    image = models.ImageField(null=True)


class ProductRating(models.Model):
    ''' Model for Products Rating'''
    name = models.ForeignKey(Products, on_delete=models.CASCADE)
    rating = models.FloatField(null=True)
    rated_by = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Cart(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    added_by = models.ForeignKey(Profile,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1,blank=False,null=False)
    status = models.CharField(default="Pending",max_length=50)

class Order(models.Model):
    name = models.CharField(_("Customer Name"), max_length=254, blank=False, null=False)
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = models.CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(
        _("Payment ID"), max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"
