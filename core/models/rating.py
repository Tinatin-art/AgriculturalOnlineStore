from django.db import models
from django import forms
from .product import Product
from django.contrib.auth.models import User

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),), default=5)
    created_at =  models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']