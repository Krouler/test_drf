# Generated by Django 4.1.7 on 2023-06-28 08:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import marketplace.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование продукта')),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Полное название')),
                ('name_short', models.CharField(blank=True, default='', max_length=20, verbose_name='Короткое название')),
                ('slug_name', models.CharField(max_length=20, unique=True, verbose_name='Название для URL')),
                ('inn', models.CharField(max_length=12, verbose_name='ИНН')),
                ('ceo', models.CharField(max_length=56, verbose_name='Фамилия И.О. руководителя')),
                ('balance', models.FloatField(blank=True, default=0.0, verbose_name='Баланс магазина')),
                ('cred_num', models.CharField(blank=True, default='', editable=False, max_length=12, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=marketplace.models.get_image_path_for_shop, verbose_name='Аватар магазина')),
                ('employee', models.ManyToManyField(related_name='shops', to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник')),
                ('main_employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='shops_maintainer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Магазин',
                'verbose_name_plural': 'Магазины',
            },
        ),
        migrations.CreateModel(
            name='Stash',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.CharField(blank=True, default='', editable=False, max_length=15, unique=True, verbose_name='Артикул')),
                ('count', models.PositiveIntegerField(blank=True, default=0, verbose_name='Количество')),
                ('cost', models.FloatField(default=0.0, verbose_name='Стоимость, в рублях')),
                ('image', models.ImageField(blank=True, null=True, upload_to=marketplace.models.get_image_path_for_stash, verbose_name='Изображение товара')),
                ('description', models.TextField(blank=True, default='', max_length=1500, verbose_name='Описание')),
                ('is_delivery_available', models.BooleanField(blank=True, default=False, verbose_name='Доступность доставки')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='shops', to='marketplace.product', verbose_name='Продукт')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='marketplace.shop', verbose_name='Магазин')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='shop',
            field=models.ManyToManyField(through='marketplace.Stash', to='marketplace.shop'),
        ),
        migrations.CreateModel(
            name='CommentShopProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='Оценка товара')),
                ('caption', models.CharField(max_length=50, verbose_name='Заголовок комментария')),
                ('description', models.TextField(max_length=1000, verbose_name='Текст комментария')),
                ('stash', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='marketplace.stash', verbose_name='Товар')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments_to_product', to=settings.AUTH_USER_MODEL, verbose_name='Комментатор')),
            ],
        ),
    ]
