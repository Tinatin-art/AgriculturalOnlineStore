from django.db import models
from django.contrib.auth.models import User
from .product import Product


class Comment(models.Model):
    
    product = models.ForeignKey(Product,
                            on_delete=models.CASCADE,
                            related_name='comments', null=True,
                            blank=True, )
    user = models.ForeignKey(User, 
                            on_delete=models.CASCADE,
                            related_name='user', null=True,
                            blank=True, )
    text = models.TextField(verbose_name='Отзыв')
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
        return f'Comment by {self.user} on {self.product}'