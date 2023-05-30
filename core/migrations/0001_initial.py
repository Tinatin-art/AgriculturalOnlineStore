# Generated by Django 4.2.1 on 2023-05-28 14:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryName', models.CharField(max_length=20, unique=True, verbose_name='Название категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='Описание')),
                ('image', models.ImageField(upload_to='', verbose_name='Рисунок')),
                ('price', models.IntegerField(default=0, verbose_name='Цена')),
                ('currency', models.CharField(default='сом', max_length=10, verbose_name='Валюта')),
                ('productivity', models.CharField(max_length=20, verbose_name='Урожайность')),
                ('unit', models.IntegerField(default=0, verbose_name='Количество')),
                ('unitName', models.CharField(choices=[('Грамм', 'Грамм'), ('Кг', 'Кг'), ('Лирт', 'Лирт'), ('Шт', 'Шт')], default='Шт', max_length=50, verbose_name='Единица измерения')),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Отзыв')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=False)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Комментария',
                'verbose_name_plural': 'Комментарии',
                'ordering': ['-created_on'],
                'indexes': [models.Index(fields=['created_on'], name='core_commen_created_6224c6_idx')],
            },
        ),
    ]
