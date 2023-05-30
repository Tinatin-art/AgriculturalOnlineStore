from django.db import models
from django.contrib.auth.models import User
<<<<<<< HEAD
from .product import Product


=======
from django import forms
from django.forms import Textarea
from .product import Product



>>>>>>> 303f2d36e89cd5c8e6ed64dd97c440eadd96dfae
class Comment(models.Model):
    
    product = models.ForeignKey(Product,
                            on_delete=models.CASCADE,
                            related_name='comments', null=True,
                            blank=True, )
    user = models.ForeignKey(User, 
                            on_delete=models.CASCADE,
                            related_name='user', null=True,
                            blank=True, )
<<<<<<< HEAD
    text = models.TextField(verbose_name='Отзыв')
=======
    text = models.TextField(verbose_name='Ваш отзыв')
>>>>>>> 303f2d36e89cd5c8e6ed64dd97c440eadd96dfae
    created_on = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Комментария'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_on']
        indexes = [
        models.Index(fields=['created_on']),
        ]


    def __str__(self):
<<<<<<< HEAD
        return f'Comment by {self.user} on {self.product}'
=======
        return f'Comment by {self.user} on {self.product}'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text',]
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['text'].widget = Textarea(attrs={'row':3, 'cols': 10,"class": "comments__textarea", 'placeholder': 'Оставьте комментарий'})  
>>>>>>> 303f2d36e89cd5c8e6ed64dd97c440eadd96dfae
