from django.db import models

class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    categoryName = models.CharField(max_length=50, unique=True, verbose_name="Категории")

    def __str__(self):
        return self.categoryName

    @staticmethod
    def get_all_categories():
        return Category.objects.all()
