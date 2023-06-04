from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg



class CustomUser(AbstractUser):
    GENDERS = (
        ('М','Мужчина'),
        ('Ж','Женщина'),
    )
    REGIONS = (
        ('Ош', 'Ош'),
        ('Баткен', 'Баткен'),
        ('Джалал-Абад', 'Джалал-Абад'),
        ('Нарын', 'Нарын'),
        ('Талас', 'Талас'),
        ('Ыссык-Куль', 'Ыссык-Куль'),
        ('Чуй', 'Чуй')
    )

    name = models.CharField('Имя', max_length=255, null=True, )
    surname = models.CharField('Фамилия', max_length=255, null=True,)
    gender = models.CharField('Пол', max_length=1, choices=GENDERS, default='', null=True,)
    region = models.CharField('Область', max_length=20, choices=REGIONS, default='Чуй', null=True)
    address = models.CharField('Адрес',max_length=255, null=True, )
    city = models.CharField('Город', max_length=255, null=True,)
    country = models.CharField('Страна', max_length=255, null=True,)
    email = models.EmailField('Почта', max_length=255, null=True, unique=True)
    phone = models.CharField('Контакты', max_length=255, null=True,)
    image = models.ImageField('Фотография', upload_to='profile_photo', null=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'gender', ]

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['-created_at']



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

class Product(models.Model):

    gram = "Грамм"
    kilograms = "Кг"
    liter = 'Лирт'
    amount = 'Шт'

    UNITNAME_CHOICES = (
        (gram, "Грамм"),
        (kilograms, "Кг"),
        (liter, "Лирт"),
        (amount, 'Шт')
    )

    name = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, verbose_name='Категория')
    description = models.CharField('Описание', max_length=500, default='', null=True, blank=True)
    image = models.ImageField('Фотография', upload_to='')
    price = models.IntegerField('Цена', default=0)
    currency = models.CharField('Валюта', max_length=10, default="сом")
    productivity = models.CharField('Урожайность', max_length=20)
    unit = models.IntegerField('Количество', default=0)
    unitName = models.CharField('Единица измерения', 
        max_length=50,
        choices=UNITNAME_CHOICES,
        default=amount, 
    )
    average_rating = models.DecimalField('Средний рейтинг', max_digits=2, decimal_places=1, default=5)
       
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
    
    def update_average_rating(self):
        average_rating = self.rating_set.aggregate(Avg('rating')).get('rating__avg')
        if average_rating is not None:
            self.average_rating = round(average_rating, 1)
        else:
            self.average_rating = 0
        self.save()




class Comment(models.Model):    
    product = models.ForeignKey(Product,
                            on_delete=models.CASCADE,
                            related_name='comments', null=True,
                            blank=True, )
    user = models.ForeignKey(CustomUser, 
                            on_delete=models.CASCADE,
                            related_name='user', null=True,
                            blank=True, )
    text = models.TextField('Отзыв')
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



class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),), default=5)
    created_at =  models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Order(models.Model):
    ORDERED = 'ordered'
    SHIPPED = 'shipped'

    STATUS_CHOICES = (
        (ORDERED, 'Ordered'),
        (SHIPPED, 'Shipped')
    )

    user = models.ForeignKey(CustomUser, related_name='orders', blank=True, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)
    paid_amount = models.IntegerField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED)
    ordered = models.BooleanField(default=False)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.order}'
