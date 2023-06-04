from django.db import models
from .category import Category
from django.db.models import Avg

class Product(models.Model):

    gram = "гр"
    kilograms = "кг"
    liter = 'литр'
    pcs = 'шт'


    UNITNAME_CHOICES = [
        (gram, "грамм"),
        (kilograms, "килограмм"),
        (liter, "литр"),
        (pcs, "штук")

    ]

    name = models.CharField(max_length=20, verbose_name="Продукт")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, verbose_name="Категория")
    description = models.CharField(max_length=200, default='', null=True, blank=True)
    image = models.ImageField(upload_to='')
    rate = models.IntegerField(default=0)
    price = models.IntegerField(default=0, verbose_name="Цена")
    currency = models.CharField(max_length=10, default="сом")
    productivity = models.CharField(max_length=20, blank=True)
    unit = models.IntegerField(default=0)
    unitName = models.CharField(
        max_length=50,
        choices=UNITNAME_CHOICES,
        default=gram,
    )

    average_rating = models.DecimalField('Средний рейтинг', max_digits=2, decimal_places=1, default=5)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


    def __str__(self):
        return self.name


    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)

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
    

    def update_average_rating(self):
        average_rating = self.rating_set.aggregate(Avg('rating')).get('rating__avg')
        if average_rating is not None:
            self.average_rating = round(average_rating, 1)
        else:
            self.average_rating = 0
        self.save()
  