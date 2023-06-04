# Generated by Django 4.2.1 on 2023-06-04 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_product_average_rating_alter_rating_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='average_rating',
            field=models.DecimalField(decimal_places=1, default=5, max_digits=3, verbose_name='Средний рейтинг'),
        ),
    ]
