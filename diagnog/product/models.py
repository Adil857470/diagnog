from django.db import models
from user.models import Profile

# Create your models here.
from datetime import datetime


class Products(models.Model):
    ''' Model for Products '''
    name = models.CharField(max_length=255, null=True)
    base_price = models.CharField(max_length=100, null=True)
    discounted_price = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def getImage(self):
        # image = ProductImages.objects.filter()
        image = ProductImages.objects.filter(name=self.id).first()
        image_url = 'https://diagnog-media.s3.us-east-1.amazonaws.com/' + \
            str(image.image)

        return image_url

    def getRatings(self):
        all_rating = ProductRating.objects.filter(name=self.id)
        return all_rating


class ProductImages(models.Model):
    ''' Model for Products Images'''
    name = models.ForeignKey(Products, on_delete=models.CASCADE)
    image = models.ImageField(null=True)


class ProductRating(models.Model):
    ''' Model for Products Rating'''
    name = models.ForeignKey(Products, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True)
    rated_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
