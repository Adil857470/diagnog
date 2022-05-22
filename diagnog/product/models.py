from django.db import models
from user.models import Profile

# Create your models here.
from datetime import datetime
from django.db.models import Avg


class Products(models.Model):
    ''' Model for Products '''
    name = models.CharField(max_length=255, null=True)
    base_price = models.CharField(max_length=100, null=True)
    discounted_price = models.CharField(max_length=100, null=True)
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


class Orders(models.Model):
    ''' Model for Products Order'''
    methods = (('UPI', 'UPI'), ('NetBanking', 'NetBanking'))
    name = models.ForeignKey(Products, on_delete=models.CASCADE)
    order_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order_date = models.DateTimeField(auto_now=True)
    cod = models.BooleanField(default=False)
    payment_method = models.CharField(
        max_length=150, blank=True, null=True, choices=methods)
