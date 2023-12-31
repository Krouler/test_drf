# Generated by Django 4.1.7 on 2023-06-29 09:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import marketplace.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('marketplace', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='shop',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='shop',
            name='main_employee',
        ),
        migrations.AlterField(
            model_name='shop',
            name='cred_num',
            field=models.CharField(blank=True, default='', editable=False, max_length=12, unique=True, verbose_name='Внутренний номер счета'),
        ),
        migrations.CreateModel(
            name='ConfidentialInfoShop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.FloatField(blank=True, default=0.0, verbose_name='Баланс магазина')),
                ('employee', models.ManyToManyField(related_name='shops', to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник')),
                ('main_employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='shops_maintainer', to=settings.AUTH_USER_MODEL)),
                ('shop', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='confdata', to='marketplace.shop')),
            ],
        ),
    ]
