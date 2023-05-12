from django.db import models

class Category(models.Model):
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    categoryName = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.categoryName

    @staticmethod
    def get_all_categories():
        return Category.objects.all()
