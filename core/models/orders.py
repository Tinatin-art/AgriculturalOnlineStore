from django.contrib.auth.models import User
from django.db import models

from .product import Product

class Order(models.Model):

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    ORDERED = 'ordered'
    SHIPPED = 'shipped'

    STATUS_CHOICES = (
        (ORDERED, 'Ordered'),
        (SHIPPED, 'Shipped')
    )

    user = models.ForeignKey(User, related_name='orders', blank=True, null=True, on_delete=models.CASCADE, verbose_name="Пользователь")
    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, verbose_name="Почта")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    zipcode = models.CharField(max_length=255, verbose_name="Почтовый индекс")
    place = models.CharField(max_length=255, verbose_name="Город")
    phone = models.CharField(max_length=255, verbose_name="Номер тел")

    created_at = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)
    paid_amount = models.IntegerField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED, verbose_name="Статус")

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)