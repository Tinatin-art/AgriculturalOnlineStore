# Generated by Django 4.2.1 on 2023-05-18 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
    ]
