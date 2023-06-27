from random import randrange

from django.contrib.auth.models import User
from django.db import models


def make_result(lim, prefix=''):
    result = prefix
    while len(result) < lim:
        result += str(randrange(10))
    return result


def get_qs_list(model, only_field):
    return model.objects.only(only_field).values_list(only_field, flat=True)


def randomize_product_article():
    qs_list = get_qs_list(Product, 'article')
    result_ = ''
    while result_ in qs_list or result_ == '':
        result_ = make_result(15, 'A')
    return result_


def randomize_cred_num():
    qs_list = get_qs_list(Shop, 'cred_num')
    result_ = ''
    while result_ in qs_list or result_ == '':
        result_ = make_result(12)
    return result_


def get_image_path_for_stash(instance, filename):
    return 'shops_{0}/stash/{1}/{2}'.format(instance.shop.id, instance.article, filename)


def get_image_path_for_shop(instance, filename):
    return 'shops_{0}/image/{1}'.format(instance.shop.id, filename)


class Shop(models.Model):
    name = models.CharField(null=False, blank=False, verbose_name='Полное название')
    name_short = models.CharField(null=False, blank=True, default='', verbose_name='Короткое название')
    slug_name = models.CharField(null=False, unique=True, blank=False, max_length=20, verbose_name='Название для URL')
    inn = models.CharField(max_length=12, null=False, blank=False, verbose_name='ИНН')
    ceo = models.CharField(max_length=56, null=False, blank=False, verbose_name='Фамилия И.О. руководителя')
    balance = models.FloatField(default=0.0, blank=True, verbose_name='Баланс магазина')
    main_employee = models.ForeignKey(User, related_name='shops_maintainer', on_delete=models.PROTECT)
    employee = models.ManyToManyField(User, related_name='shops', verbose_name='Сотрудник',
                                      on_delete=models.SET_NULL, null=True)
    cred_num = models.CharField(max_length=12, default=randomize_cred_num, blank=True, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Дата и время создания')
    avatar = models.ImageField(upload_to=get_image_path_for_shop, null=True, blank=True, verbose_name='Аватар магазина')

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.name_short


class Product(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name='Наименование продукта')
    shop = models.ManyToManyField(Shop, through='Stash')


class Stash(models.Model):
    article = models.CharField(max_length=15, default=randomize_product_article, blank=True, editable=False,
                               unique=True, verbose_name='Артикул')
    product = models.ForeignKey(Product, related_name='shops', verbose_name='Продукт', on_delete=models.PROTECT)
    shop = models.ForeignKey(Shop, related_name='products', on_delete=models.CASCADE, verbose_name='Магазин')
    count = models.PositiveIntegerField(default=0, blank=True, verbose_name='Количество')
    image = models.ImageField(upload_to=get_image_path_for_stash, null=True, blank=True,
                              verbose_name='Изображение товара')
    description = models.TextField(default='', blank=True, verbose_name='Описание', max_length=1500)
    is_delivery_available = models.BooleanField(default=False, blank=True, verbose_name='Доступность доставки')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Дата создания')

