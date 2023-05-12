from django.db import models
from .category import Category

class Product(models.Model):

    gram = "g"
    kilograms = "kg"
    liter = 'liter'

    UNITNAME_CHOICES = [
        (gram, "gram"),
        (kilograms, "kilograms"),
        (liter, "liter"),
    ]

    name = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200, default='', null=True, blank=True)
    image = models.ImageField(upload_to='')
    rate = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    currency = models.CharField(max_length=10, default="сом")
    productivity = models.CharField(max_length=20)
    unit = models.IntegerField(default=0)
    unitName = models.CharField(
        max_length=50,
        choices=UNITNAME_CHOICES,
        default=gram,
    )
    

    @staticmethod
    def get_all_products():
        return Product.objects.all()
    

    @staticmethod
    def get_all_products_by_categoryId(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()
  