from django.db import models
from .category import Category   

class Product(models.Model):

    gram = "Грамм"
    kilograms = "Кг"
    liter = 'Лирт'
    amount = 'Шт'

    UNITNAME_CHOICES = [
        (gram, "Грамм"),
        (kilograms, "Кг"),
        (liter, "Лирт"),
        (amount, 'Шт')
    ]

    name = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, verbose_name='Категория')
    description = models.CharField(max_length=500, default='', null=True, blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='', verbose_name='Рисунок')
    price = models.IntegerField(default=0,verbose_name='Цена')
    currency = models.CharField(max_length=10, default="сом",verbose_name='Валюта')
    productivity = models.CharField(max_length=20, verbose_name='Урожайность')
    unit = models.IntegerField(default=0, verbose_name='Количество')
    unitName = models.CharField(
        max_length=50,
        choices=UNITNAME_CHOICES,
        default=amount,
        verbose_name='Единица измерения'
    )
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


    def __str__(self):
        return self.name

    @staticmethod
    def get_all_products():
        return Product.objects.all()
    

    @staticmethod
    def get_all_products_by_categoryId(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()
    
    def get_absolute_url(self):
        return f'/detail/{self.id}'