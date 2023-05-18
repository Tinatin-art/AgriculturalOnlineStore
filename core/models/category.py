from django.db import models

class Category(models.Model):
    categoryName = models.CharField('Название категории', max_length=20, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.categoryName

    @staticmethod
    def get_all_categories():
        return Category.objects.all()
    
    # def get_absolute_url(self):
    #     return f'/detail/{self.id}'
  