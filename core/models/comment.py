from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.forms import Textarea
from .product import Product



class Comment(models.Model):
    
    product = models.ForeignKey(Product,
                            on_delete=models.CASCADE,
                            related_name='comments', null=True,
                            blank=True, verbose_name="Продукт" )
    user = models.ForeignKey(User, 
                            on_delete=models.CASCADE,
                            related_name='user', null=True,
                            blank=True, verbose_name="Пользователь" )
    text = models.TextField(verbose_name='Ваш отзыв')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False, verbose_name="Статус")

    class Meta:
        verbose_name = 'Комментария'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_on']
        indexes = [
        models.Index(fields=['created_on']),
        ]


    def __str__(self):
        return f'Comment by {self.user} on {self.product}'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text',]
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['text'].widget = Textarea(attrs={'row':3, 'cols': 10,"class": "comments__textarea", 'placeholder': 'Оставьте комментарий'})  