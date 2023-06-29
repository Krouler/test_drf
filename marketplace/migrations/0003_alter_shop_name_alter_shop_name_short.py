# Generated by Django 4.1.7 on 2023-06-29 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0002_remove_shop_balance_remove_shop_employee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='name',
            field=models.CharField(max_length=150, unique=True, verbose_name='Полное название'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='name_short',
            field=models.CharField(blank=True, default='', max_length=20, unique=True, verbose_name='Короткое название'),
        ),
    ]
